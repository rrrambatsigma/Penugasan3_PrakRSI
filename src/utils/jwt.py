from datetime import datetime, timedelta, timezone
from jose import jwt

SECRET_KEY = "super-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


def create_access_token(data: dict):
    to_encode = data.copy()

    # ✅ pastikan sub itu string (fix utama)
    if not isinstance(to_encode.get("sub"), str):
        to_encode["sub"] = str(to_encode["sub"])

    expire = datetime.now(timezone.utc) + timedelta(minutes=60)
    to_encode.update({"exp": expire})

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)