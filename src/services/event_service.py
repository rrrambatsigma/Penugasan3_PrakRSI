from sqlmodel import Session, select
from src.repositories.event_repository import EventRepository
from src.database.schema import Event
from datetime import datetime
from fastapi import HTTPException


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
            # ✅ VALIDASI NAME
            if not data.name or data.name.strip() == "":
                raise HTTPException(400, "Event name is required")

            # ✅ VALIDASI DESCRIPTION
            if not data.description or data.description.strip() == "":
                raise HTTPException(400, "Description is required")

            # ✅ VALIDASI WAKTU LOGIKA TAMBAHAN
            if data.started_at < datetime.now():
                raise HTTPException(400, "Event start time cannot be in the past")

            event = Event(
                **data.dict(),
                created_at=datetime.now(),
                updated_at=datetime.now()
            )

            return self.repo.create(db, event)

        except HTTPException as e:
            raise e

        except Exception as e:
            raise HTTPException(500, f"Failed to create event: {str(e)}")


    def update_event(self, db: Session, event_id: int, data):
        try:
            event = self.repo.get_by_id(db, event_id)

            if not event:
                raise HTTPException(404, "Event not found")

            # ✅ VALIDASI
            if not data.name or data.name.strip() == "":
                raise HTTPException(400, "Event name cannot be empty")

            if not data.description or data.description.strip() == "":
                raise HTTPException(400, "Description cannot be empty")

            if data.started_at < datetime.now():
                raise HTTPException(400, "Event start time cannot be in the past")

            event.name = data.name
            event.description = data.description
            event.quota = data.quota
            event.started_at = data.started_at
            event.ended_at = data.ended_at
            event.updated_at = datetime.now()

            return self.repo.update(db, event)

        except HTTPException as e:
            raise e

        except Exception as e:
            raise HTTPException(500, f"Failed to update event: {str(e)}")


    def delete_event(self, db: Session, event_id: int):
        try:
            event = self.repo.get_by_id(db, event_id)

            if not event:
                raise HTTPException(404, "Event not found")

            self.repo.delete(db, event)
            return event

        except HTTPException as e:
            raise e

        except Exception as e:
            raise HTTPException(500, f"Failed to delete event: {str(e)}")


    def patch_event(self, db: Session, event_id: int, data):
        try:
            event = self.repo.get_by_id(db, event_id)

            if not event:
                raise HTTPException(404, "Event not found")

            update_data = data.model_dump(exclude_unset=True)

            # ✅ VALIDASI PARTIAL
            if "name" in update_data:
                if not update_data["name"] or update_data["name"].strip() == "":
                    raise HTTPException(400, "Event name cannot be empty")

            if "description" in update_data:
                if not update_data["description"] or update_data["description"].strip() == "":
                    raise HTTPException(400, "Description cannot be empty")

            if "started_at" in update_data:
                if update_data["started_at"] < datetime.now():
                    raise HTTPException(400, "Start time cannot be in the past")

            if "started_at" in update_data and "ended_at" in update_data:
                if update_data["ended_at"] <= update_data["started_at"]:
                    raise HTTPException(400, "End time must be after start time")

            for key, value in update_data.items():
                setattr(event, key, value)

            event.updated_at = datetime.now()

            return self.repo.update(db, event)

        except HTTPException as e:
            raise e

        except Exception as e:
            raise HTTPException(500, f"Failed to patch event: {str(e)}")


    def search_events(self, db: Session, name=None, location=None):
        try:
            statement = select(Event)

            if name:
                statement = statement.where(Event.name.contains(name))

            if location:
                statement = statement.where(Event.location.contains(location))

            return db.exec(statement).all()

        except Exception as e:
            raise HTTPException(500, f"Search failed: {str(e)}")