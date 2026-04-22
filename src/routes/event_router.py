from fastapi import APIRouter, Depends
from src.controllers import event_controller
from src.utils.auth import require_role
from src.database.schema.schema import User, RoleEnum
from src.dto.event import EventCreate
from sqlmodel import Session
from src.database.connection import get_session

router = APIRouter(prefix="/events", tags=["Events"])

# PUBLIC / BEBAS
@router.get("/")
def get_events():
    return event_controller.get_events()

@router.get("/search")
def search_events():
    return event_controller.search_events()

@router.get("/{event_id}")
def get_event(event_id: int):
    return event_controller.get_event(event_id)


# ADMIN ONLY
@router.post("/")
def create_event(
    request: EventCreate,
    db: Session = Depends(get_session),
    user: User = Depends(require_role([RoleEnum.ADMIN]))
):
    return event_controller.create_event(request)

@router.put("/{event_id}")
def update_event(
    event_id: int,
    user: User = Depends(require_role([RoleEnum.ADMIN]))
):
    return event_controller.update_event(event_id)

@router.delete("/{event_id}")
def delete_event(
    event_id: int,
    user: User = Depends(require_role([RoleEnum.ADMIN]))
):
    return event_controller.delete_event(event_id)

@router.patch("/{event_id}")
def patch_event(
    event_id: int,
    user: User = Depends(require_role([RoleEnum.ADMIN]))
):
    return event_controller.patch_event(event_id)