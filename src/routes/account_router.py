from fastapi import APIRouter
from src.controllers import account_controller

router = APIRouter(prefix="/accounts", tags=["Accounts"])

router.get("/")(account_controller.get_accounts)
router.get("/{account_id}")(account_controller.get_account)
router.post("/")(account_controller.create_account)
router.delete("/{account_id}")(account_controller.delete_account)
router.patch("/{account_id}")(account_controller.patch_account)