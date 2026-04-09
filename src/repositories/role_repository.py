from sqlmodel import Session, select
from src.database.schema import Role
from sqlalchemy.exc import IntegrityError
from src.database.schema import Role


def create_role(db: Session, role: Role):
    db.add(role)
    db.commit()
    db.refresh(role)
    return role

def get_all_roles(db: Session):
    return db.exec(select(Role)).all()

def get_role_by_id(db: Session, role_id: int):
    return db.get(Role, role_id)

def delete_role(db: Session, role: Role):
    try:
        db.delete(role)
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Role masih digunakan di tabel lain"
        )