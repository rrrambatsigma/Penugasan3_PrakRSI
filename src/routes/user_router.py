from fastapi import APIRouter, Depends
from src.utils.auth import get_current_user
from src.controllers import user_controller

router = APIRouter(prefix="/users", tags=["Users"])

# READ (Daftar User)
router.get("/", dependencies=[Depends(get_current_user)])(user_controller.get_users)
router.get("/search", dependencies=[Depends(get_current_user)])(user_controller.search_users)
router.get("/{user_id}", dependencies=[Depends(get_current_user)])(user_controller.get_user)

# UPDATE & DELETE
router.put("/{user_id}", dependencies=[Depends(get_current_user)])(user_controller.update_user)
router.patch("/{user_id}", dependencies=[Depends(get_current_user)])(user_controller.patch_user)
router.delete("/{user_id}", dependencies=[Depends(get_current_user)])(user_controller.delete_user)