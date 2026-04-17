from fastapi import FastAPI
from sqlmodel import Session, select

from src.database.connection import init_db, engine
from src.database.schema.schema import Role, RoleEnum

from src.routes.register import router as register_router
from src.routes.login import router as login_router
from src.routes import (
    user_router, 
    account_router,
    role_router,
    registration_router,
    event_router,
    register
)

app = FastAPI(title="Acara RSI API")


# =========================
# INIT DB
# =========================
init_db()


# =========================
# SEED ROLE (AUTO)
# =========================
def seed_roles():
    with Session(engine) as db:
        for role_name in RoleEnum:
            existing = db.exec(
                select(Role).where(Role.name == role_name)
            ).first()

            if not existing:
                db.add(Role(name=role_name))

        db.commit()


@app.on_event("startup")
def on_startup():
    seed_roles()


# =========================
# ROOT
# =========================
@app.get("/")
def root():
    return {"message": "API is running 🚀"}


# =========================
# ROUTES
# =========================
app.include_router(role_router.router)
app.include_router(user_router.router)
app.include_router(account_router.router)
app.include_router(event_router.router)
app.include_router(registration_router.router)
app.include_router(register.router)
app.include_router(register_router)
app.include_router(login_router)