from sqlmodel import Session, select
from src.database.schema.schema import Registration

def create_registration(db: Session, registration: Registration):
    db.add(registration)
    db.commit()
    db.refresh(registration)
    return registration

def get_all_registrations(db: Session):
    return db.exec(select(Registration)).all()

def get_registration_by_id(db: Session, registration_id: int):
    return db.get(Registration, registration_id)

def delete_registration(db: Session, registration: Registration):
    db.delete(registration)
    db.commit()