from fastapi import APIRouter, Depends
from sqlmodel import Session

from src.database.connection import get_session

from src.dto.register import (
    RegisterRequest,
    RegisterSuccessResponse
)

from src.controllers.register import register_controller

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]  # 🔥 lebih jelas dari "Auth"
)


@router.post(
    "/register",
    response_model=RegisterSuccessResponse,
    status_code=201
)
def register_endpoint(
    request: RegisterRequest,   # 🔥 ganti nama biar konsisten
    db: Session = Depends(get_session)
):
    return register_controller(db, request)