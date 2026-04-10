from fastapi import APIRouter
from src.controllers import user_controller

router = APIRouter(prefix="/users", tags=["Users"])

router.get("/")(user_controller.get_users)
router.get("/search")(user_controller.search_users)
router.get("/{user_id}")(user_controller.get_user)

router.post("/")(user_controller.create_user)
router.put("/{user_id}")(user_controller.update_user)
router.delete("/{user_id}")(user_controller.delete_user)
router.patch("/{user_id}")(user_controller.patch_user)