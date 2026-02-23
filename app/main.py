from fastapi import FastAPI
from app.routers import auth,users
from app.db.session import SessionLocal, engine
from app.db.base import Base

from app.models import user

app = FastAPI(title="SMS FastAPI")

app.include_router(auth.router)
app.include_router(users.router)

Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    return {"message": "School Management System API is running!"}