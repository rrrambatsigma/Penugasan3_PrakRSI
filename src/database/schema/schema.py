from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional, List
from enum import Enum


# =========================
# ENUM ROLE
# =========================
class RoleEnum(str, Enum):
    ADMIN = "admin"
    USER = "user"


# =========================
# ROLE
# =========================
class Role(SQLModel, table=True):
    __tablename__ = "roles"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: RoleEnum = Field(index=True, unique=True)

    accounts: List["Account"] = Relationship(back_populates="role")


# =========================
# USER (AUTH UTAMA 🔥)
# =========================
class User(SQLModel, table=True):
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)

    username: str = Field(index=True, max_length=50)
    email: str = Field(index=True, unique=True)
    password: str

    first_name: Optional[str] = Field(default=None, max_length=255)
    last_name: Optional[str] = Field(default=None, max_length=255)
    whatsapp: Optional[str] = Field(default=None, max_length=30)

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # 🔥 RELATION
    account: Optional["Account"] = Relationship(back_populates="user")
    registrations: List["Registration"] = Relationship(back_populates="user")


# =========================
# ACCOUNT (ROLE HOLDER)
# =========================
class Account(SQLModel, table=True):
    __tablename__ = "accounts"

    id: Optional[int] = Field(default=None, primary_key=True)

    user_id: int = Field(foreign_key="users.id")
    role_id: int = Field(foreign_key="roles.id")

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    user: Optional["User"] = Relationship(back_populates="account")
    role: Optional["Role"] = Relationship(back_populates="accounts")

    logs: List["Log"] = Relationship(back_populates="account")


# =========================
# EVENT
# =========================
class Event(SQLModel, table=True):
    __tablename__ = "events"

    id: Optional[int] = Field(default=None, primary_key=True)

    name: Optional[str] = None
    description: Optional[str] = None
    quota: Optional[int] = None

    started_at: Optional[datetime] = None
    ended_at: Optional[datetime] = None

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    registrations: List["Registration"] = Relationship(back_populates="event")


# =========================
# REGISTRATION
# =========================
class Registration(SQLModel, table=True):
    __tablename__ = "registrations"

    id: Optional[int] = Field(default=None, primary_key=True)

    user_id: int = Field(foreign_key="users.id")
    event_id: int = Field(foreign_key="events.id")

    user: Optional["User"] = Relationship(back_populates="registrations")
    event: Optional["Event"] = Relationship(back_populates="registrations")


# =========================
# LOG
# =========================
class Log(SQLModel, table=True):
    __tablename__ = "logs"

    id: Optional[int] = Field(default=None, primary_key=True)

    account_id: int = Field(foreign_key="accounts.id")

    created_at: Optional[datetime] = None
    action: Optional[str] = None
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None

    entity: Optional[str] = None
    entity_id: Optional[int] = None

    account: Optional["Account"] = Relationship(back_populates="logs")