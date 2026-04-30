from fastapi import FastAPI
from app.routers import auth,users,admin
from app.db.session import SessionLocal, engine
from app.db.base import Base
from app.routers import academic
from app.models import user
from app.routers import student, teacher, parent
from app.routers import attendance

app = FastAPI(title="SMS FastAPI")

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(admin.router)
app.include_router(academic.router)
app.include_router(student.router)
app.include_router(teacher.router)
app.include_router(parent.router)
app.include_router(attendance.router)

Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    return {"message": "School Management System API is running!"}