from fastapi import Depends
from sqlmodel import Session

from src.database.connection import get_session
from src.dto.account import AccountCreate, AccountPatch
from src.services.account_service import (
    create_account_service,
    get_all_accounts_service,
    get_account_by_id_service,
    delete_account_service,
    patch_account_service
)


def get_accounts(db: Session = Depends(get_session)):
    return get_all_accounts_service(db)


def get_account(account_id: int, db: Session = Depends(get_session)):
    return get_account_by_id_service(db, account_id)


def create_account(data: AccountCreate, db: Session = Depends(get_session)):
    return create_account_service(db, data)


def delete_account(account_id: int, db: Session = Depends(get_session)):
    return delete_account_service(db, account_id)

def patch_account(account_id: int, data: AccountPatch, db: Session = Depends(get_session)):
    return patch_account_service(db, account_id, data)