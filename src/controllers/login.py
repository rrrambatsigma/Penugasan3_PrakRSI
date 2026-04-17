from sqlmodel import Session

from src.dto.login import LoginRequest, LoginResponse
from src.services.login import login_user


def login_controller(db: Session, request: LoginRequest):
    token = login_user(db, request.email, request.password)

    return LoginResponse(
        access_token=token
    )