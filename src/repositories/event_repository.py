from sqlmodel import Session, select
from src.database.schema.schema import Event


class EventRepository:

    def get_all(self, db: Session):
        return db.exec(select(Event)).all()

    def get_by_id(self, db: Session, event_id: int):
        return db.get(Event, event_id)

    def create(self, db: Session, event: Event):
        db.add(event)
        db.commit()
        db.refresh(event)
        return event

    def update(self, db: Session, event: Event):
        db.add(event)
        db.commit()
        db.refresh(event)
        return event

    def delete(self, db: Session, event: Event):
        db.delete(event)
        db.commit()