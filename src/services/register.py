from sqlmodel import Session
from datetime import datetime

from src.utils.hash import hash_password

from src.database.schema.schema import User, Account

from src.repositories.user_repository import (
    create_user,
    get_user_by_email,
    get_user_by_username
)

from src.repositories.role_repository import get_role_user
from src.repositories.account_repository import create_account


def register_account(db: Session, data):
    # =========================
    # VALIDASI DUPLICATE
    # =========================
    if get_user_by_email(db, data.email):
        raise Exception("Email sudah digunakan")

    if get_user_by_username(db, data.username):
        raise Exception("Username sudah digunakan")

    # =========================
    # HASH PASSWORD (ARGON2)
    # =========================
    hashed_password = hash_password(data.password)

    # =========================
    # AMBIL ROLE USER DEFAULT
    # =========================
    role = get_role_user(db)
    if not role:
        raise Exception("Role USER belum ada di database")

    now = datetime.now()

    # =========================
    # CREATE USER (FULL DATA ✅)
    # =========================
    user = User(
        username=data.username,
        email=data.email,
        password=hashed_password,
        role_id=role.id,
        first_name=data.first_name,
        last_name=data.last_name,
        whatsapp=data.whatsapp,
        created_at=now,
        updated_at=now
    )

    user = create_user(db, user)

    # =========================
    # CREATE ACCOUNT (OPSIONAL)
    # =========================
    account = Account(
        user_id=user.id,
        role_id=role.id
    )
    create_account(db, account)

    # =========================
    # RETURN OBJECT (PENTING 🔥)
    # =========================
    return user