from fastapi import Depends
from sqlmodel import Session

from src.database.connection import get_session
from src.dto.role import RoleCreate, RoleUpdate, RolePatch
from src.services.role_service import (
    create_role_service,
    get_all_roles_service,
    get_role_by_id_service,
    delete_role_service,
    update_role_service,
    patch_role_service
)


def get_roles(db: Session = Depends(get_session)):
    return get_all_roles_service(db)


def get_role(role_id: int, db: Session = Depends(get_session)):
    return get_role_by_id_service(db, role_id)


def create_role(data: RoleCreate, db: Session = Depends(get_session)):
    return create_role_service(db, data)


def delete_role(role_id: int, db: Session = Depends(get_session)):
    return delete_role_service(db, role_id)

def update_role(role_id: int, data: RoleUpdate, db: Session = Depends(get_session)):
    return update_role_service(db, role_id, data)

def patch_role(role_id: int, data: RolePatch, db: Session = Depends(get_session)):
    return patch_role_service(db, role_id, data)