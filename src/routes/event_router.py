from fastapi import APIRouter
from src.controllers import event_controller

router = APIRouter(prefix="/events", tags=["Events"])

router.get("/")(event_controller.get_events)

router.get("/search")(event_controller.search_events)

router.get("/{event_id}")(event_controller.get_event)

router.post("/")(event_controller.create_event)
router.put("/{event_id}")(event_controller.update_event)
router.delete("/{event_id}")(event_controller.delete_event)
router.patch("/{event_id}")(event_controller.patch_event)