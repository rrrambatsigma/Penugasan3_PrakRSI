from jose import JWTError, jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlmodel import Session
from fastapi import Depends, HTTPException, status
from src.database.connection import get_session
from src.database.schema.schema import User, RoleEnum

SECRET_KEY = "super-secret-key"
ALGORITHM = "HS256"

oauth2_scheme = HTTPBearer()


def get_current_user(
    auth: HTTPAuthorizationCredentials = Depends(oauth2_scheme),
    session: Session = Depends(get_session)
):
    if auth is None or auth.credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token tidak ditemukan"
        )

    token = auth.credentials

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        user_id: str | None = payload.get("sub")

        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token invalid (sub tidak ada)"
            )

    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Token invalid: {str(e)}"
        )

    user = session.get(User, int(user_id))

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User tidak ditemukan"
        )

    return user


def require_role(allowed_roles: list[RoleEnum]):
    def role_checker(user: User = Depends(get_current_user)):

        if not user.account or not user.account.role:
            raise HTTPException(
                status_code=403,
                detail="User tidak memiliki role"
            )

        user_role = user.account.role.name  # enum

        if user_role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User tidak memiliki role"
            )

        user_role = user.account.role.name  # enum

        if user_role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Akses ditolak untuk role: {user_role}"
            )

        return user

    return role_checker