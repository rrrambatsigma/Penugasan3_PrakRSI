from typing import Optional
from fastapi import Depends, Query
from sqlmodel import Session

from src.database.connection import get_session
from src.services.registration_service import search_registrations_service
from src.dto.registration import RegistrationCreate, RegistrationPatch
from src.services.registration_service import (
    create_registration_service,
    get_all_registrations_service,
    get_registration_by_id_service,
    delete_registration_service,
    patch_registration_service

)


def get_registrations(db: Session = Depends(get_session)):
    return get_all_registrations_service(db)


def get_registration(registration_id: int, db: Session = Depends(get_session)):
    return get_registration_by_id_service(db, registration_id)


def create_registration(data: RegistrationCreate, db: Session = Depends(get_session)):
    return create_registration_service(db, data)


def delete_registration(registration_id: int, db: Session = Depends(get_session)):
    return delete_registration_service(db, registration_id)

def search_registrations(
    user_id: Optional[int] = Query(None),
    event_id: Optional[int] = Query(None),
    db: Session = Depends(get_session)
):
    return search_registrations_service(db, user_id, event_id)

def patch_registration(registration_id: int, data: RegistrationPatch, db: Session = Depends(get_session)):
    return patch_registration_service(db, registration_id, data)