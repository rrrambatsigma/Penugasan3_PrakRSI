from typing import Optional
from fastapi import Depends, Query
from sqlmodel import Session

from src.database.connection import get_session
from src.dto.user import UserCreate, UserUpdate, UserPatch
from src.services.user_service import (
    create_user_service,
    get_all_users_service,
    get_user_by_id_service,
    update_user_service,
    delete_user_service,
    search_users_service,
    patch_user_service
)


def get_users(db: Session = Depends(get_session)):
    return get_all_users_service(db)


def get_user(user_id: int, db: Session = Depends(get_session)):
    return get_user_by_id_service(db, user_id)


def create_user(data: UserCreate, db: Session = Depends(get_session)):
    return create_user_service(db, data)


def update_user(user_id: int, data: UserUpdate, db: Session = Depends(get_session)):
    return update_user_service(db, user_id, data)


def delete_user(user_id: int, db: Session = Depends(get_session)):
    return delete_user_service(db, user_id)

def search_users(
    name: Optional[str] = Query(None),
    email: Optional[str] = Query(None),
    db: Session = Depends(get_session)
):
    return search_users_service(db, name, email)

def patch_user(user_id: int, data: UserPatch, db: Session = Depends(get_session)):
    return patch_user_service(db, user_id, data)