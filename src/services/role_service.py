from sqlmodel import Session
from fastapi import HTTPException
from src.database.schema.schema import Role
from src.repositories.role_repository import (
    create_role,
    get_all_roles,
    get_role_by_id,
    delete_role
)

def create_role_service(db: Session, data):
    try:
        if not data.name or data.name.strip() == "":
            raise HTTPException(status_code=400, detail="Role name is required")

        # OPTIONAL: normalize
        data.name = data.name.strip()

        role = Role(**data.model_dump())
        return create_role(db, role)

    except HTTPException as e:
        raise e

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create role: {str(e)}")


def get_all_roles_service(db: Session):
    try:
        return get_all_roles(db)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch roles: {str(e)}")


def get_role_by_id_service(db: Session, role_id: int):
    try:
        role = get_role_by_id(db, role_id)

        if not role:
            raise HTTPException(status_code=404, detail="Role not found")

        return role

    except HTTPException as e:
        raise e

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching role: {str(e)}")


def delete_role_service(db: Session, role_id: int):
    try:
        role = get_role_by_id(db, role_id)

        if not role:
            raise HTTPException(status_code=404, detail="Role not found")

        delete_role(db, role)
        return {"message": "Role deleted successfully"}

    except HTTPException as e:
        raise e

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete role: {str(e)}")


def update_role_service(db: Session, role_id: int, data):
    try:
        role = get_role_by_id(db, role_id)

        if not role:
            raise HTTPException(status_code=404, detail="Role not found")

        if not data.name or data.name.strip() == "":
            raise HTTPException(status_code=400, detail="Role name cannot be empty")

        role.name = data.name.strip()

        db.add(role)
        db.commit()
        db.refresh(role)

        return role

    except HTTPException as e:
        raise e

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update role: {str(e)}")


def patch_role_service(db: Session, role_id: int, data):
    try:
        role = get_role_by_id(db, role_id)

        if not role:
            raise HTTPException(status_code=404, detail="Role not found")

        update_data = data.model_dump(exclude_unset=True)

        if "name" in update_data:
            if not update_data["name"] or update_data["name"].strip() == "":
                raise HTTPException(status_code=400, detail="Role name cannot be empty")

            update_data["name"] = update_data["name"].strip()

        for key, value in update_data.items():
            setattr(role, key, value)

        db.add(role)
        db.commit()
        db.refresh(role)

        return role

    except HTTPException as e:
        raise e

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to patch role: {str(e)}")