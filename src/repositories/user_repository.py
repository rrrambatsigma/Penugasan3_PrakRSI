from sqlmodel import Session, select
from src.database.schema import User

# CREATE
def create_user(db: Session, user: User):
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

# GET ALL
def get_all_users(db: Session):
    return db.exec(select(User)).all()

# GET BY ID
def get_user_by_id(db: Session, user_id: int):
    return db.get(User, user_id)

# UPDATE
def update_user(db: Session, user_id: int, user_data):
    user = db.get(User, user_id)
    
    if not user:
        return None

     # update field sesuai UserUpdate
    if user_data.first_name is not None:
        user.first_name = user_data.first_name
    if user_data.last_name is not None:
        user.last_name = user_data.last_name
    if user_data.whatsapp is not None:
        user.whatsapp = user_data.whatsapp

    db.add(user)
    db.commit()
    db.refresh(user)
    return user

# DELETE
def delete_user(db: Session, user: User):
    db.delete(user)
    db.commit()