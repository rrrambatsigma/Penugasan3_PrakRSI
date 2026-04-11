from sqlmodel import Session, select
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException

from src.database.schema.schema import Role
from src.database.schema.schema import RoleEnum


def create_role(db: Session, role: Role):
    db.add(role)
    db.commit()
    db.refresh(role)
    return role


def get_all_roles(db: Session):
    return db.exec(select(Role)).all()


def get_role_by_id(db: Session, role_id: int):
    return db.get(Role, role_id)


# 🔥 TAMBAHAN (UMUM DIPAKAI DI REGISTER)
def get_role_by_name(db: Session, role_name: str):
    statement = select(Role).where(Role.name == role_name)
    return db.exec(statement).first()


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


# 🔥 KHUSUS REGISTER (DEFAULT USER)
def get_role_user(db: Session):
    statement = select(Role).where(Role.name == RoleEnum.USER)
    return db.exec(statement).first()