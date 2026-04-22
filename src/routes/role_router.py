from fastapi import APIRouter, Depends
from src.controllers import role_controller
from src.utils.auth import require_role
from src.database.schema.schema import User, RoleEnum
from src.dto.role import RoleCreate


router = APIRouter(prefix="/roles", tags=["Roles"])

@router.post("/")
def create_role(request: RoleCreate):
    return role_controller.create_role(request)

@router.get("/")
def get_roles():
    return role_controller.get_roles()

@router.get("/{role_id}")
def get_role(role_id: int):
    return role_controller.get_role(role_id)


@router.post("/")
def create_role(
    user: User = Depends(require_role([RoleEnum.ADMIN]))
):
    return role_controller.create_role()

@router.put("/{role_id}")
def update_role(
    role_id: int,
    user: User = Depends(require_role([RoleEnum.ADMIN]))
):
    return role_controller.update_role(role_id)

@router.delete("/{role_id}")
def delete_role(
    role_id: int,
    user: User = Depends(require_role([RoleEnum.ADMIN]))
):
    return role_controller.delete_role(role_id)

@router.patch("/{role_id}")
def patch_role(
    role_id: int,
    user: User = Depends(require_role([RoleEnum.ADMIN]))
):
    return role_controller.patch_role(role_id)