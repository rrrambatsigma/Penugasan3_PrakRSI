from datetime import datetime
from fastapi import HTTPException
from sqlmodel import Session
from src.database.schema.schema import Account, User, Role
from src.repositories.account_repository import (
    create_account,
    get_account_by_id,
    get_all_accounts,
    delete_account
)

def create_account_service(db: Session, account_data):
    try:
        user = db.get(User, account_data.user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        role = db.get(Role, account_data.role_id)
        if not role:
            raise HTTPException(status_code=404, detail="Role not found")

        if not account_data.email or account_data.email.strip() == "":
            raise HTTPException(status_code=400, detail="Email is required")

        if "@" not in account_data.email:
            raise HTTPException(status_code=400, detail="Invalid email format")

        if not account_data.username or account_data.username.strip() == "":
            raise HTTPException(status_code=400, detail="Username is required")

        if len(account_data.username) < 3:
            raise HTTPException(status_code=400, detail="Username too short")

        if not account_data.password or account_data.password.strip() == "":
            raise HTTPException(status_code=400, detail="Password is required")

        if len(account_data.password) < 6:
            raise HTTPException(status_code=400, detail="Password must be at least 6 characters")

        now = datetime.now()
        account = Account(
            **account_data.dict(),
            created_at=now,
            updated_at=now,
        )

        return create_account(db, account)

    except HTTPException as e:
        raise e

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create account: {str(e)}")


def get_all_accounts_service(db: Session):
    try:
        return get_all_accounts(db)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch accounts: {str(e)}")


def get_account_by_id_service(db: Session, account_id: int):
    try:
        account = get_account_by_id(db, account_id)

        if not account:
            raise HTTPException(status_code=404, detail="Account not found")

        return account

    except HTTPException as e:
        raise e

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching account: {str(e)}")


def delete_account_service(db: Session, account_id: int):
    try:
        account = get_account_by_id(db, account_id)

        if not account:
            raise HTTPException(status_code=404, detail="Account not found")

        delete_account(db, account)
        return {"message": "Account deleted successfully"}

    except HTTPException as e:
        raise e

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete account: {str(e)}")


def patch_account_service(db: Session, account_id: int, data):
    try:
        account = get_account_by_id(db, account_id)

        if not account:
            raise HTTPException(status_code=404, detail="Account not found")

        update_data = data.model_dump(exclude_unset=True)

        
        if "username" in update_data:
            if not update_data["username"] or update_data["username"].strip() == "":
                raise HTTPException(status_code=400, detail="Username cannot be empty")

            if len(update_data["username"]) < 3:
                raise HTTPException(status_code=400, detail="Username too short")

        
        if "password" in update_data:
            if len(update_data["password"]) < 6:
                raise HTTPException(status_code=400, detail="Password must be at least 6 characters")

        for key, value in update_data.items():
            setattr(account, key, value)

        account.updated_at = datetime.now()

        db.add(account)
        db.commit()
        db.refresh(account)

        return account

    except HTTPException as e:
        raise e

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to patch account: {str(e)}")