from pydantic import BaseModel


class ParentCreate(BaseModel):
    user_id: int