from fastapi import APIRouter
from src.controllers import role_controller

router = APIRouter(prefix="/roles", tags=["Roles"])

router.get("/")(role_controller.get_roles)
router.get("/{role_id}")(role_controller.get_role)
router.post("/")(role_controller.create_role)
router.put("/{role_id}")(role_controller.update_role)
router.delete("/{role_id}")(role_controller.delete_role)
router.patch("/{role_id}")(role_controller.patch_role)