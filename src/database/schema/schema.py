from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional


class Role(SQLModel, table=True):
    __tablename__ = "roles"

    id: int = Field(default=None, primary_key=True)
    name: str = Field(max_length=255)

    accounts: list["Account"] = Relationship(back_populates="role")


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: int = Field(default=None, primary_key=True)
    first_name: str = Field(default=None, max_length=255)
    last_name: str = Field(default=None, max_length=255)
    whatsapp: str = Field(default=None, max_length=30)
    created_at: datetime = None
    updated_at: datetime = None

    accounts: list["Account"] = Relationship(back_populates="user")
    registrations: list["Registration"] = Relationship(back_populates="user")


class Account(SQLModel, table=True):
    __tablename__ = "accounts"

    id: int = Field(default=None, primary_key=True)

    user_id: int = Field(default=None, foreign_key="users.id")
    role_id: int = Field(default=None, foreign_key="roles.id")

    email: str = None
    username: str = Field(default=None, max_length=16)
    password: str = None

    created_at: datetime = None
    updated_at: datetime = None

    user: Optional[User] = Relationship(back_populates="accounts")
    role: Optional[Role] = Relationship(back_populates="accounts")

    logs: list["Log"] = Relationship(back_populates="account")


class Event(SQLModel, table=True):
    __tablename__ = "events"

    id: int = Field(default=None, primary_key=True)

    name: str = None
    description: str = None
    quota: int = None

    started_at: datetime = None
    ended_at: datetime = None

    created_at: datetime = None
    updated_at: datetime = None

    registrations: list["Registration"] = Relationship(back_populates="event")


class Registration(SQLModel, table=True):
    __tablename__ = "registrations"

    id: int = Field(default=None, primary_key=True)

    user_id: int = Field(default=None, foreign_key="users.id")
    event_id: int = Field(default=None, foreign_key="events.id")

    user: Optional[User] = Relationship(back_populates="registrations")
    event: Optional[Event] = Relationship(back_populates="registrations")


class Log(SQLModel, table=True):
    __tablename__ = "logs"

    id: int = Field(default=None, primary_key=True)

    account_id: int = Field(default=None, foreign_key="accounts.id")

    created_at: datetime = None
    action: str = None
    ip_address: str = None
    user_agent: str = None

    entity: str = None
    entity_id: int = None

    account: Optional[Account] = Relationship(back_populates="logs")