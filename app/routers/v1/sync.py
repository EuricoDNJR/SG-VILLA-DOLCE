import logging
import json
import os
from urllib import request, error

from pydantic import BaseModel
from fastapi import APIRouter, Depends, Header, status
from fastapi.responses import JSONResponse
from typing import Optional

from database import models
from database.crud.sync import (
    claim_sync_events,
    get_inbound_event_by_key,
    get_pending_sync_events,
    get_pending_sync_summary,
    ingest_remote_sync_event,
    mark_sync_event_done,
    mark_sync_event_failed,
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
    if (
        sync_event.entity == "pedido"
        and sync_event.operation == "create"
        and isinstance(payload_data, dict)
        and not payload_data.get("clienteSnapshot")
    ):
        cliente_snapshot = _build_cliente_snapshot(payload_data.get("idCliente"))
        if cliente_snapshot:
            payload_data["clienteSnapshot"] = cliente_snapshot

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
        try:
            error_body = http_error.read().decode("utf-8")
        except Exception:
            error_body = ""
        return False, f"http_error={http_error.code} body={error_body}"
    except Exception as req_error:
        return False, str(req_error)


def _is_remote_api_key_valid(x_api_key: Optional[str]):
    expected_key = os.getenv("SYNC_REMOTE_API_KEY", "").strip()
    if not expected_key:
        return True
    return bool(x_api_key and x_api_key.strip() == expected_key)


@router.post(
    "/push_pending/",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(get_token_header)],
)
def push_pending(limit: int = 25):
    try:
        events = claim_sync_events(limit=limit)

        if not events:
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={"processed": 0, "done": 0, "failed": 0, "message": "Sem eventos pendentes"},
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
            },
        )
    except Exception as e:
        logging.error(e)
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": "Erro ao processar fila de sincronizacao: " + str(e)},
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
        logging.error(e)
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": "Erro ao ingerir evento de sincronizacao: " + str(e)},
        )
