from fastapi import HTTPException
from sqlmodel import Session

from src.services.register import register_account
from src.dto.register import (
    RegisterRequest,
    RegisterResponse,
    RegisterSuccessResponse
)


def register_controller(db: Session, request: RegisterRequest):
    try:
        # =========================
        # CALL SERVICE
        # =========================
        user = register_account(db, request)

        # =========================
        # FORMAT RESPONSE
        # =========================
        response_data = RegisterResponse(
            id=user.id,
            username=user.username,
            email=user.email
        )

        return RegisterSuccessResponse(
            message="Register success",
            data=response_data
        )

    except HTTPException as e:
        # 🔥 BIAR ERROR DARI SERVICE TIDAK KE-OVERRIDE
        raise e

    except Exception as e:
        # =========================
        # HANDLE ERROR GENERAL
        # =========================
        raise HTTPException(
            status_code=500,
            detail=f"Internal Server Error: {str(e)}"
        )