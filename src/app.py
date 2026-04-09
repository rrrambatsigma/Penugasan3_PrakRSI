from fastapi import FastAPI
from src.database.connection import init_db
from src.routes import (
    user_router, 
    account_router,
    role_router,
    registration_router,
    event_router
)

app = FastAPI(title="Acara RSI API")

# Init DB tables
init_db()

# Root
@app.get("/")
def root():
    return {"message": "API is running 🚀"}

# URUTAN SESUAI RELASI DATABASE
app.include_router(role_router.router)
app.include_router(user_router.router)
app.include_router(account_router.router)
app.include_router(event_router.router)
app.include_router(registration_router.router)