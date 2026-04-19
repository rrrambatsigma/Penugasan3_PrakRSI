from fastapi import APIRouter, Depends
from src.utils.auth import get_current_user
from src.controllers import account_controller

router = APIRouter(prefix="/accounts", tags=["Accounts"])

router.get("/", dependencies=[Depends(get_current_user)])(account_controller.get_accounts)
router.get("/{account_id}", dependencies=[Depends(get_current_user)])(account_controller.get_account)
router.post("/", dependencies=[Depends(get_current_user)])(account_controller.create_account)
router.delete("/{account_id}", dependencies=[Depends(get_current_user)])(account_controller.delete_account)
router.patch("/{account_id}", dependencies=[Depends(get_current_user)])(account_controller.patch_account)