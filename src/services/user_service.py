from fastapi import HTTPException
from sqlmodel import Session, select
from src.database.schema.schema import User
from datetime import datetime
from src.repositories.user_repository import (
    create_user,
    get_user_by_id,
    get_all_users,
    delete_user,
    update_user
)

def create_user_service(db: Session, user_data):
    try:
        if not user_data.first_name or user_data.first_name.strip() == "":
            raise HTTPException(status_code=400, detail="First name is required")

        if not user_data.whatsapp or user_data.whatsapp.strip() == "":
            raise HTTPException(status_code=400, detail="Whatsapp is required")

        if not user_data.whatsapp.isdigit():
            raise HTTPException(status_code=400, detail="Whatsapp must be numeric")

        if len(user_data.whatsapp) < 10:
            raise HTTPException(status_code=400, detail="Whatsapp number is too short")

        now = datetime.now()
        user = User(
            **user_data.dict(),
            created_at=now,
            updated_at=now,
        )

        return create_user(db, user)

    except HTTPException as e:
        raise e

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create user: {str(e)}")


def update_user_service(db: Session, user_id: int, user_data):
    try:
        user = update_user(db, user_id, user_data)

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        if user_data.first_name is not None:
            if user_data.first_name.strip() == "":
                raise HTTPException(status_code=400, detail="First name cannot be empty")

        if user_data.whatsapp is not None:
            if not user_data.whatsapp.isdigit():
                raise HTTPException(status_code=400, detail="Whatsapp must be numeric")

        user.updated_at = datetime.now()

        db.add(user)
        db.commit()
        db.refresh(user)

        return user

    except HTTPException as e:
        raise e

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update user: {str(e)}")


def get_all_users_service(db: Session):
    try:
        return get_all_users(db)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch users: {str(e)}")


def get_user_by_id_service(db: Session, user_id: int):
    try:
        user = get_user_by_id(db, user_id)

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        return user

    except HTTPException as e:
        raise e

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching user: {str(e)}")


def delete_user_service(db: Session, user_id: int):
    try:
        user = get_user_by_id(db, user_id)

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        delete_user(db, user)
        return {"message": "User deleted successfully"}

    except HTTPException as e:
        raise e

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete user: {str(e)}")


def search_users_service(db: Session, name: str = None, email: str = None):
    try:
        query = select(User)

        if name:
            query = query.where(User.name.contains(name))

        if email:
            query = query.where(User.email.contains(email))

        return db.exec(query).all()

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")


def patch_user_service(db: Session, user_id: int, data):
    try:
        user = get_user_by_id(db, user_id)

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        update_data = data.model_dump(exclude_unset=True)

        if "name" in update_data:
            if not update_data["name"] or update_data["name"].strip() == "":
                raise HTTPException(status_code=400, detail="Name cannot be empty")

        if "email" in update_data:
            if "@" not in update_data["email"]:
                raise HTTPException(status_code=400, detail="Invalid email format")

        for key, value in update_data.items():
            setattr(user, key, value)

        db.add(user)
        db.commit()
        db.refresh(user)

        return user

    except HTTPException as e:
        raise e

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to patch user: {str(e)}")