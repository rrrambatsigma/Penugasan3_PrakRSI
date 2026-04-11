from sqlmodel import Session, select
from src.database.schema.schema import User


def create_user(db: Session, user: User):
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_all_users(db: Session):
    statement = select(User)
    return db.exec(statement).all()


def get_user_by_id(db: Session, user_id: int):
    return db.get(User, user_id)


# 🔥 TAMBAHAN (UNTUK REGISTER)
def get_user_by_email(db: Session, email: str):
    statement = select(User).where(User.email == email)
    return db.exec(statement).first()


def get_user_by_username(db: Session, username: str):
    statement = select(User).where(User.username == username)
    return db.exec(statement).first()


def update_user(db: Session, user_id: int, user_data: dict):
    user = db.get(User, user_id)

    if not user:
        return None

    for key, value in user_data.items():
        setattr(user, key, value)

    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def delete_user(db: Session, user: User):
    db.delete(user)
    db.commit()
    return True