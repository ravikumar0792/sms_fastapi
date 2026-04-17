from pydantic import BaseModel


class SubjectCreate(BaseModel):
    name: str
    class_id: int


class SubjectOut(BaseModel):
    id: int
    name: str
    class_id: int

    class Config:
        from_attributes = True