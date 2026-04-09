from typing import Optional
from datetime import datetime
from fastapi import Depends, Query
from sqlmodel import Session

from src.services.event_service import EventService
from src.database.connection import get_session
from src.dto.event import EventCreate, EventPatch


service = EventService()


def get_events(db: Session = Depends(get_session)):
    return service.get_events(db)


def get_event(event_id: int, db: Session = Depends(get_session)):
    return service.get_event(db, event_id)


def create_event(data: EventCreate, db: Session = Depends(get_session)):
    return service.create_event(db, data)


def update_event(event_id: int, data: EventCreate, db: Session = Depends(get_session)):
    return service.update_event(db, event_id, data)


def delete_event(event_id: int, db: Session = Depends(get_session)):
    return service.delete_event(db, event_id)

def search_events(
    name: Optional[str] = Query(None),
    started_at: Optional[datetime] = Query(None),
    ended_at: Optional[datetime] = Query(None),
    db: Session = Depends(get_session)
):
    return service.search_events(db, name, started_at, ended_at)

def patch_event(event_id: int, data: EventPatch, db: Session = Depends(get_session)):
    return service.patch_event(db, event_id, data)