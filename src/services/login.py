from fastapi import HTTPException
from sqlmodel import Session

from src.repositories.user_repository import get_user_by_email
from src.utils.hash import verify_password
from src.utils.jwt import create_access_token


def login_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)

    if not user:
        raise HTTPException(status_code=401, detail="Email tidak ditemukan")

    if not verify_password(password, user.password):
        raise HTTPException(status_code=401, detail="Password salah")

    if not user.account:
        raise HTTPException(status_code=401, detail="Account user tidak ditemukan")

    token = create_access_token({
        "sub": str(user.id),
        "email": user.email,
        "username": user.username,
        "role_id": user.account.role_id
    })

    return token