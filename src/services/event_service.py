from sqlmodel import Session, select
from src.repositories.event_repository import EventRepository
from src.database.schema import Event
from datetime import datetime
from fastapi import HTTPException
from datetime import datetime, timezone


class EventService:

    def __init__(self):
        self.repo = EventRepository()

    def get_events(self, db: Session):
        try:
            return self.repo.get_all(db)
        except Exception as e:
            raise HTTPException(500, f"Failed to fetch events: {str(e)}")

    def get_event(self, db: Session, event_id: int):
        try:
            event = self.repo.get_by_id(db, event_id)

            if not event:
                raise HTTPException(404, "Event not found")

            return event

        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(500, f"Error fetching event: {str(e)}")


    def create_event(self, db: Session, data):
        try:
            now = datetime.now(timezone.utc)

            if not data.name or data.name.strip() == "":
                raise HTTPException(400, "Event name is required")

            if not data.description or data.description.strip() == "":
                raise HTTPException(400, "Description is required")

            if data.started_at < now:
                raise HTTPException(400, "Event start time cannot be in the past")

            if data.ended_at <= data.started_at:
                raise HTTPException(400, "End time must be after start time")

            event = Event(
                **data.dict(),
                created_at=now,
                updated_at=now
            )

            return self.repo.create(db, event)

        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(500, f"Failed to create event: {str(e)}")

    def update_event(self, db: Session, event_id: int, data):
        try:
            now = datetime.now()
            event = self.repo.get_by_id(db, event_id)

            if not event:
                raise HTTPException(404, "Event not found")

            # 🔥 FIX TIMEZONE
            if data.started_at:
                data.started_at = data.started_at.replace(tzinfo=None)

            if data.ended_at:
                data.ended_at = data.ended_at.replace(tzinfo=None)

            if not data.name or data.name.strip() == "":
                raise HTTPException(400, "Event name cannot be empty")

            if not data.description or data.description.strip() == "":
                raise HTTPException(400, "Description cannot be empty")

            if data.started_at < now:
                raise HTTPException(400, "Event start time cannot be in the past")

            if data.ended_at <= data.started_at:
                raise HTTPException(400, "End time must be after start time")

            event.name = data.name
            event.description = data.description
            event.quota = data.quota
            event.started_at = data.started_at
            event.ended_at = data.ended_at
            event.updated_at = now

            return self.repo.update(db, event)

        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(500, f"Failed to update event: {str(e)}")