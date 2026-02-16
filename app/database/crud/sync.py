import json
import uuid
from datetime import datetime

from database import models


def enqueue_sync_event(entity: str, entity_id: str, operation: str, payload: dict):
    idempotency_key = str(uuid.uuid4())

    return models.SyncQueue.create(
        entity=entity,
        entityId=str(entity_id) if entity_id is not None else None,
        operation=operation,
        payloadJson=json.dumps(payload, ensure_ascii=False),
        idempotencyKey=idempotency_key,
        status="pending",
        attempts=0,
        lastError=None,
        createdAt=datetime.utcnow(),
        updatedAt=datetime.utcnow(),
    )


def get_pending_sync_summary():
    pending_count = (
        models.SyncQueue.select().where(models.SyncQueue.status == "pending").count()
    )
    failed_count = (
        models.SyncQueue.select().where(models.SyncQueue.status == "failed").count()
    )
    processing_count = (
        models.SyncQueue.select().where(models.SyncQueue.status == "processing").count()
    )

    return {
        "pending": pending_count,
        "failed": failed_count,
        "processing": processing_count,
        "total": pending_count + failed_count + processing_count,
    }


def get_pending_sync_events(limit=50):
    events = (
        models.SyncQueue.select()
        .where(models.SyncQueue.status.in_(["pending", "failed", "processing"]))
        .order_by(models.SyncQueue.createdAt.asc())
        .limit(limit)
    )

    return [
        {
            "idSyncEvent": str(event.idSyncEvent),
            "entity": event.entity,
            "entityId": event.entityId,
            "operation": event.operation,
            "status": event.status,
            "attempts": event.attempts,
            "lastError": event.lastError,
            "createdAt": event.createdAt.isoformat() if event.createdAt else None,
            "updatedAt": event.updatedAt.isoformat() if event.updatedAt else None,
        }
        for event in events
    ]


def claim_sync_events(limit=25):
    events = (
        models.SyncQueue.select()
        .where(models.SyncQueue.status.in_(["pending", "failed"]))
        .order_by(models.SyncQueue.createdAt.asc())
        .limit(limit)
    )

    claimed = []
    now = datetime.utcnow()

    for event in events:
        event.status = "processing"
        event.updatedAt = now
        event.save()
        claimed.append(event)

    return claimed


def mark_sync_event_done(event):
    event.status = "done"
    event.lastError = None
    event.updatedAt = datetime.utcnow()
    event.save()


def mark_sync_event_failed(event, error_message: str):
    event.status = "failed"
    event.attempts += 1
    event.lastError = str(error_message)[:2000]
    event.updatedAt = datetime.utcnow()
    event.save()


def ingest_remote_sync_event(
    *,
    idempotency_key: str,
    entity: str,
    entity_id: str,
    operation: str,
    payload: dict,
    source: str = "remote_client",
):
    existing_event = models.SyncInboundEvent.get_or_none(
        models.SyncInboundEvent.idempotencyKey == idempotency_key
    )

    if existing_event:
        return existing_event, False

    created_event = models.SyncInboundEvent.create(
        idempotencyKey=idempotency_key,
        entity=entity,
        entityId=str(entity_id) if entity_id is not None else None,
        operation=operation,
        payloadJson=json.dumps(payload, ensure_ascii=False),
        source=source,
        createdAt=datetime.utcnow(),
    )
    return created_event, True


def get_inbound_event_by_key(idempotency_key: str):
    return models.SyncInboundEvent.get_or_none(
        models.SyncInboundEvent.idempotencyKey == idempotency_key
    )
