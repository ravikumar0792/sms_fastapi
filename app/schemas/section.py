from pydantic import BaseModel


class SectionCreate(BaseModel):
    name: str
    class_id: int


class SectionOut(BaseModel):
    id: int
    name: str
    class_id: int

    class Config:
        from_attributes = True