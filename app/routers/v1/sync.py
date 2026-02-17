import logging
import json
import os
import traceback
from datetime import datetime
from urllib.parse import quote
from urllib import request, error

from pydantic import BaseModel
from fastapi import APIRouter, Depends, Header, status
from fastapi.responses import JSONResponse
from typing import Optional

from database import models
from database.crud.sync import (
    claim_sync_events,
    get_checkpoint_timestamp,
    get_inbound_event_by_key,
    get_outbound_event_by_key,
    get_pending_sync_events,
    get_pending_sync_summary,
    ingest_remote_sync_event,
    mark_sync_event_done,
    mark_sync_event_failed,
    requeue_stale_processing_events,
    upsert_checkpoint_timestamp,
)
from database.crud.sync_apply import apply_sync_event
from dependencies import get_token_header

router = APIRouter()


def _build_cliente_snapshot(id_cliente: str):
    if not id_cliente:
        return None

    cliente = models.Cliente.get_or_none(models.Cliente.idCliente == id_cliente)
    if cliente is None:
        return None

    return {
        "idCliente": str(cliente.idCliente),
        "email": cliente.email,
        "nome": cliente.nome,
        "dataNascimento": str(cliente.dataNascimento)
        if cliente.dataNascimento is not None
        else None,
        "cpf": cliente.cpf,
        "endereco": cliente.endereco,
        "telefone": cliente.telefone,
        "saldo": float(cliente.saldo) if cliente.saldo is not None else 0.0,
    }


def _build_produtos_snapshot(produtos_payload):
    if not isinstance(produtos_payload, list):
        return []

    snapshots = []
    for item in produtos_payload:
        produto_id = (item or {}).get("idProduto")
        if not produto_id:
            continue

        produto = models.Produto.get_or_none(models.Produto.idProduto == produto_id)
        if produto is None:
            continue

        snapshots.append(
            {
                "idProduto": str(produto.idProduto),
                "nome": produto.nome,
                "descricao": produto.descricao,
                "categoria": str(produto.categoria.idCategoria),
                "categoriaNome": produto.categoria.nome,
                "unidadeMedida": produto.categoria.unidadeMedida,
                "valorVenda": float(produto.valorVenda),
            }
        )

    return snapshots


class InboundSyncEventRequest(BaseModel):
    idSyncEvent: str
    entity: str
    entityId: Optional[str] = None
    operation: str
    payload: dict
    idempotencyKey: str
    createdAt: Optional[str] = None


@router.get(
    "/pending_summary/",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(get_token_header)],
)
def pending_summary():
    try:
        summary = get_pending_sync_summary()
        return JSONResponse(status_code=status.HTTP_200_OK, content=summary)
    except Exception as e:
        logging.error(e)
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": "Erro ao buscar resumo de sincronizacao: " + str(e)},
        )


@router.get(
    "/pending_events/",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(get_token_header)],
)
def pending_events(limit: int = 50):
    try:
        events = get_pending_sync_events(limit=limit)
        return JSONResponse(status_code=status.HTTP_200_OK, content=events)
    except Exception as e:
        logging.error(e)
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": "Erro ao buscar eventos de sincronizacao: " + str(e)},
        )


def _push_event_to_remote(sync_event):
    remote_enabled = os.getenv("SYNC_REMOTE_ENABLED", "OFF").strip().upper() == "ON"
    remote_base_url = os.getenv("SYNC_REMOTE_BASE_URL", "").strip().rstrip("/")
    remote_api_key = os.getenv("SYNC_REMOTE_API_KEY", "").strip()

    if not remote_enabled:
        return False, "SYNC_REMOTE_ENABLED=OFF"

    if not remote_base_url:
        return False, "SYNC_REMOTE_BASE_URL vazio"

    payload_data = json.loads(sync_event.payloadJson)
    if sync_event.entity == "pedido" and isinstance(payload_data, dict):
        if sync_event.operation == "create" and not payload_data.get("clienteSnapshot"):
            cliente_snapshot = _build_cliente_snapshot(payload_data.get("idCliente"))
            if cliente_snapshot:
                payload_data["clienteSnapshot"] = cliente_snapshot

        if sync_event.operation in ["create", "add_items"] and not payload_data.get("produtosSnapshot"):
            payload_data["produtosSnapshot"] = _build_produtos_snapshot(payload_data.get("idProdutos"))

    payload = {
        "idSyncEvent": str(sync_event.idSyncEvent),
        "entity": sync_event.entity,
        "entityId": sync_event.entityId,
        "operation": sync_event.operation,
        "payload": payload_data,
        "idempotencyKey": sync_event.idempotencyKey,
        "createdAt": sync_event.createdAt.isoformat() if sync_event.createdAt else None,
    }

    target_url = remote_base_url + "/v1/sync/events"
    req = request.Request(
        target_url,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            **({"x-api-key": remote_api_key} if remote_api_key else {}),
        },
        method="POST",
    )

    try:
        with request.urlopen(req, timeout=5) as response:
            return (200 <= response.status < 300), f"http_status={response.status}"
    except error.HTTPError as http_error:
        status_code = getattr(http_error, "code", "unknown")
        reason = getattr(http_error, "reason", "")
        body_preview = ""
        try:
            error_body_bytes = http_error.read()
            body_preview = error_body_bytes.decode("utf-8", errors="replace")
        except Exception:
            body_preview = ""
        details = [
            f"http_error={status_code}",
            f"reason={reason}" if reason else "",
            f"entity={sync_event.entity}",
            f"operation={sync_event.operation}",
            f"idSyncEvent={sync_event.idSyncEvent}",
            f"entityId={sync_event.entityId}" if sync_event.entityId else "",
            f"body={body_preview}" if body_preview else "",
        ]
        return False, " ".join(part for part in details if part)
    except Exception as req_error:
        return (
            False,
            f"request_error={str(req_error)} entity={sync_event.entity} "
            f"operation={sync_event.operation} idSyncEvent={sync_event.idSyncEvent}",
        )


def _is_remote_api_key_valid(x_api_key: Optional[str]):
    expected_key = os.getenv("SYNC_REMOTE_API_KEY", "").strip()
    if not expected_key:
        return True
    return bool(x_api_key and x_api_key.strip() == expected_key)


def _parse_iso_datetime(raw_value: Optional[str]):
    if not raw_value:
        return None
    try:
        normalized = raw_value.replace("Z", "+00:00")
        return datetime.fromisoformat(normalized)
    except Exception:
        return None


def _fetch_remote_inbound_events(*, since: Optional[str] = None, limit: int = 200):
    remote_enabled = os.getenv("SYNC_REMOTE_ENABLED", "OFF").strip().upper() == "ON"
    remote_base_url = os.getenv("SYNC_REMOTE_BASE_URL", "").strip().rstrip("/")
    remote_api_key = os.getenv("SYNC_REMOTE_API_KEY", "").strip()

    if not remote_enabled:
        return False, "SYNC_REMOTE_ENABLED=OFF", []
    if not remote_base_url:
        return False, "SYNC_REMOTE_BASE_URL vazio", []

    query_parts = [f"limit={max(1, min(int(limit), 1000))}"]
    if since:
        query_parts.append(f"since={quote(since, safe='')}")
    target_url = remote_base_url + "/v1/sync/inbound_events?" + "&".join(query_parts)

    req = request.Request(
        target_url,
        headers={
            "Content-Type": "application/json",
            **({"x-api-key": remote_api_key} if remote_api_key else {}),
        },
        method="GET",
    )

    try:
        with request.urlopen(req, timeout=10) as response:
            if not (200 <= response.status < 300):
                return False, f"http_status={response.status}", []
            payload = json.loads(response.read().decode("utf-8"))
            events = payload.get("events") if isinstance(payload, dict) else []
            if not isinstance(events, list):
                events = []
            return True, "ok", events
    except error.HTTPError as http_error:
        try:
            error_body = http_error.read().decode("utf-8", errors="replace")
        except Exception:
            error_body = ""
        return False, f"http_error={http_error.code} body={error_body}", []
    except Exception as req_error:
        return False, f"request_error={str(req_error)}", []


@router.post(
    "/push_pending/",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(get_token_header)],
)
def push_pending(limit: int = 25):
    try:
        rescued_processing = requeue_stale_processing_events(max_age_seconds=60)
        events = claim_sync_events(limit=limit)

        if not events:
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "processed": 0,
                    "done": 0,
                    "failed": 0,
                    "rescuedProcessing": rescued_processing,
                    "message": "Sem eventos pendentes",
                },
            )

        done_count = 0
        failed_count = 0

        for event in events:
            ok, info = _push_event_to_remote(event)
            if ok:
                mark_sync_event_done(event)
                done_count += 1
            else:
                mark_sync_event_failed(event, info)
                failed_count += 1

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "processed": len(events),
                "done": done_count,
                "failed": failed_count,
                "rescuedProcessing": rescued_processing,
            },
        )
    except Exception as e:
        logging.error(e)
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": "Erro ao processar fila de sincronizacao: " + str(e)},
        )


@router.get(
    "/inbound_events",
    status_code=status.HTTP_200_OK,
)
def inbound_events(
    since: Optional[str] = None,
    limit: int = 200,
    x_api_key: str = Header(default=None),
):
    try:
        if not _is_remote_api_key_valid(x_api_key):
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"message": "Invalid sync API key"},
            )

        since_dt = _parse_iso_datetime(since)
        query = models.SyncInboundEvent.select().order_by(models.SyncInboundEvent.createdAt.asc())
        if since_dt is not None:
            query = query.where(models.SyncInboundEvent.createdAt > since_dt)
        query = query.limit(max(1, min(limit, 1000)))

        events = [
            {
                "idInboundEvent": str(event.idInboundEvent),
                "idempotencyKey": event.idempotencyKey,
                "entity": event.entity,
                "entityId": event.entityId,
                "operation": event.operation,
                "payload": json.loads(event.payloadJson),
                "source": event.source,
                "createdAt": event.createdAt.isoformat() if event.createdAt else None,
            }
            for event in query
        ]

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"events": events, "count": len(events)},
        )
    except Exception as e:
        logging.error(e)
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": "Erro ao exportar eventos de sincronizacao: " + str(e)},
        )


@router.post(
    "/pull_remote/",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(get_token_header)],
)
def pull_remote(limit: int = 200):
    try:
        checkpoint_scope = "remote_inbound_sync"
        checkpoint_ts = get_checkpoint_timestamp(checkpoint_scope)
        since = checkpoint_ts.isoformat() if checkpoint_ts else None

        ok, info, events = _fetch_remote_inbound_events(since=since, limit=limit)
        if not ok:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"message": "Erro ao puxar eventos remotos: " + info},
            )

        applied = 0
        skipped = 0
        failed = 0
        latest_ts = checkpoint_ts

        for event in events:
            event_key = event.get("idempotencyKey")
            event_created_at = _parse_iso_datetime(event.get("createdAt"))
            if event_created_at and (latest_ts is None or event_created_at > latest_ts):
                latest_ts = event_created_at

            if not event_key:
                failed += 1
                continue

            # Avoid echoing back events this client originally produced.
            if get_outbound_event_by_key(event_key):
                skipped += 1
                continue

            if get_inbound_event_by_key(event_key):
                skipped += 1
                continue

            try:
                apply_sync_event(
                    entity=event.get("entity"),
                    operation=event.get("operation"),
                    payload=event.get("payload") or {},
                    entity_id=event.get("entityId"),
                )
                ingest_remote_sync_event(
                    idempotency_key=event_key,
                    entity=event.get("entity"),
                    entity_id=event.get("entityId"),
                    operation=event.get("operation"),
                    payload=event.get("payload") or {},
                    source=event.get("source") or "remote_pull",
                )
                applied += 1
            except Exception as apply_error:
                failed += 1
                logging.error("pull_remote apply error: %s", str(apply_error))

        if latest_ts is not None:
            upsert_checkpoint_timestamp(checkpoint_scope, latest_ts)

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "fetched": len(events),
                "applied": applied,
                "skipped": skipped,
                "failed": failed,
                "checkpoint": latest_ts.isoformat() if latest_ts else None,
            },
        )
    except Exception as e:
        logging.error(e)
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": "Erro ao processar pull remoto: " + str(e)},
        )


@router.post(
    "/events",
    status_code=status.HTTP_201_CREATED,
)
def ingest_sync_event(data: InboundSyncEventRequest, x_api_key: str = Header(default=None)):
    try:
        if not _is_remote_api_key_valid(x_api_key):
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"message": "Invalid sync API key"},
            )

        existing_event = get_inbound_event_by_key(data.idempotencyKey)
        if existing_event:
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "status": "duplicate",
                    "idInboundEvent": str(existing_event.idInboundEvent),
                },
            )

        apply_sync_event(
            entity=data.entity,
            operation=data.operation,
            payload=data.payload,
            entity_id=data.entityId,
        )

        created_event, created = ingest_remote_sync_event(
            idempotency_key=data.idempotencyKey,
            entity=data.entity,
            entity_id=data.entityId,
            operation=data.operation,
            payload=data.payload,
            source="desktop_client",
        )

        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={
                "status": "accepted" if created else "duplicate",
                "idInboundEvent": str(created_event.idInboundEvent),
            },
        )
    except Exception as e:
        logging.error("Erro ao ingerir evento de sync")
        logging.error(str(e))
        logging.error(traceback.format_exc())
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": "Erro ao ingerir evento de sincronizacao: " + str(e)},
        )
