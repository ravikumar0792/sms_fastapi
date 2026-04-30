from pydantic import BaseModel


class StudentCreate(BaseModel):
    user_id: int
    class_id: int
    section_id: int
    roll_number: str