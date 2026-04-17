from fastapi import APIRouter, Depends
from sqlmodel import Session

from src.database.connection import get_session
from src.dto.login import LoginRequest, LoginResponse
from src.controllers.login import login_controller

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post("/login", response_model=LoginResponse)
def login_endpoint(
    request: LoginRequest,
    db: Session = Depends(get_session)
):
    return login_controller(db, request)