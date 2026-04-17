from pydantic import BaseModel


class ClassCreate(BaseModel):
    name: str


class ClassOut(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True

