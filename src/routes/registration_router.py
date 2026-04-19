from fastapi import APIRouter, Depends
from src.utils.auth import get_current_user
from src.controllers import registration_controller

router = APIRouter(prefix="/registrations", tags=["Registrations"])

router.post("/", dependencies=[Depends(get_current_user)])(registration_controller.create_registration)
router.get("/", dependencies=[Depends(get_current_user)])(registration_controller.get_registrations)
router.get("/{registration_id}", dependencies=[Depends(get_current_user)])(registration_controller.get_registration)
router.delete("/{registration_id}", dependencies=[Depends(get_current_user)])(registration_controller.delete_registration)
router.get("/search", dependencies=[Depends(get_current_user)])(registration_controller.search_registrations)
router.patch("/{registration_id}", dependencies=[Depends(get_current_user)])(registration_controller.patch_registration)