from fastapi import APIRouter, Depends
from sqlmodel import Session
from src.database.connection import get_session
from src.utils.auth import require_role, RoleEnum
from src.dto.registration import RegistrationCreate, RegistrationResponse
from src.controllers import registration_controller
from src.utils.auth import get_current_user
from src.database.schema.schema import User

router = APIRouter(prefix="/registrations", tags=["Registrations"])


@router.post("/", response_model=RegistrationResponse,
             dependencies=[Depends(require_role([RoleEnum.USER]))])
def create_registration(
    data: RegistrationCreate,
    user: User = Depends(require_role([RoleEnum.USER]))
):
    return registration_controller.create_registration(data, user)

# HARUS LOGIN
@router.get("/")
def get_registrations(
    user: User = Depends(get_current_user)
):
    return registration_controller.get_registrations()

@router.get("/{registration_id}")
def get_registration(
    registration_id: int,
    user: User = Depends(get_current_user)
):
    return registration_controller.get_registration(registration_id)

@router.get("/search")
def search_registrations(
    user: User = Depends(get_current_user)
):
    return registration_controller.search_registrations()


# ADMIN ONLY
@router.delete("/{registration_id}")
def delete_registration(
    registration_id: int,
    user: User = Depends(require_role([RoleEnum.ADMIN]))
):
    return registration_controller.delete_registration(registration_id)

@router.patch("/{registration_id}")
def patch_registration(
    registration_id: int,
    user: User = Depends(require_role([RoleEnum.ADMIN]))
):
    return registration_controller.patch_registration(registration_id)