from fastapi import APIRouter
from src.controllers import registration_controller

router = APIRouter(prefix="/registrations", tags=["Registrations"])

router.get("/")(registration_controller.get_registrations)
router.get("/{registration_id}")(registration_controller.get_registration)
router.post("/")(registration_controller.create_registration)
router.delete("/{registration_id}")(registration_controller.delete_registration)
router.get("/search")(registration_controller.search_registrations)
router.patch("/{registration_id}")(registration_controller.patch_registration)