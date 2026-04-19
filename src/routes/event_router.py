from fastapi import APIRouter, Depends
from src.controllers import event_controller
from src.utils.auth import get_current_user
from src.database.schema.schema import User

router = APIRouter(prefix="/events", tags=["Events"])

router.get("/")(event_controller.get_events)

router.get("/search")(event_controller.search_events)

router.get("/{event_id}")(event_controller.get_event)

# Tambahkan dependencies=[Depends(get_current_user)]
router.post("/", dependencies=[Depends(get_current_user)])(event_controller.create_event)
router.put("/{event_id}", dependencies=[Depends(get_current_user)])(event_controller.update_event)
router.delete("/{event_id}", dependencies=[Depends(get_current_user)])(event_controller.delete_event)
router.patch("/{event_id}", dependencies=[Depends(get_current_user)])(event_controller.patch_event)

