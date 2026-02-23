from pydantic import BaseModel
from typing import List


class RoleCreate(BaseModel):
    name: str


class RoleUpdatePermissions(BaseModel):
    permission_ids: List[int]


class RoleOut(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class RoleWithPermissions(RoleOut):
    permissions: List[str]

    class Config:
        from_attributes = True