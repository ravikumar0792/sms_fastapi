from pydantic import BaseModel


class TeacherCreate(BaseModel):
    user_id: int