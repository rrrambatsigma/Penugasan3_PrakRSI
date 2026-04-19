from jose import JWTError, jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlmodel import Session

from src.database.connection import get_session
from src.database.schema.schema import User  # ✅ WAJIB

SECRET_KEY = "super-secret-key"
ALGORITHM = "HS256"

oauth2_scheme = HTTPBearer()


def get_current_user(
    auth: HTTPAuthorizationCredentials = Depends(oauth2_scheme),
    session: Session = Depends(get_session)
):
    print("AUTH HEADER:", auth)

    token = auth.credentials
    print("TOKEN:", token)

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print("PAYLOAD:", payload)

        user_id = payload.get("sub")
        print("USER_ID:", user_id)

        if user_id is None:
            raise HTTPException(status_code=401, detail="Token invalid")

    except JWTError as e:
        print("JWT ERROR:", str(e))
        raise HTTPException(status_code=401, detail="Token invalid")

    user = session.get(User, int(user_id))
    print("USER:", user)

    if not user:
        raise HTTPException(status_code=401, detail="User tidak ditemukan")

    return user