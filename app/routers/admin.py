from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db.deps import get_db
from app.models.role import Role
from app.models.permission import Permission
from app.models.user import User
from app.schemas.role import RoleCreate, RoleUpdatePermissions
from app.schemas.permission import PermissionCreate
from app.core.permissions import require_permission


router = APIRouter(prefix="/admin", tags=["Admin"])


@router.post(
    "/roles",
    dependencies=[Depends(require_permission("create_role"))]
)
def create_role(role: RoleCreate, db: Session = Depends(get_db)):

    existing = db.query(Role).filter(Role.name == role.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Role already exists")

    new_role = Role(name=role.name)
    db.add(new_role)
    db.commit()
    db.refresh(new_role)

    return new_role

@router.post(
    "/permissions",
    dependencies=[Depends(require_permission("create_permission"))]
)
def create_permission(permission: PermissionCreate, db: Session = Depends(get_db)):

    existing = db.query(Permission).filter(Permission.name == permission.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Permission already exists")

    new_permission = Permission(name=permission.name)
    db.add(new_permission)
    db.commit()
    db.refresh(new_permission)

    return new_permission

@router.put(
    "/roles/{role_id}/permissions",
    dependencies=[Depends(require_permission("assign_role"))]
)
def assign_permissions_to_role(
    role_id: int,
    payload: RoleUpdatePermissions,
    db: Session = Depends(get_db)
):

    role = db.query(Role).filter(Role.id == role_id).first()
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")

    permissions = db.query(Permission).filter(
        Permission.id.in_(payload.permission_ids)
    ).all()

    role.permissions = permissions  # replace existing
    db.commit()

    return {"message": "Permissions assigned successfully"}


@router.get(
    "/roles",
    dependencies=[Depends(require_permission("create_role"))]
)
def get_roles(db: Session = Depends(get_db)):

    roles = db.query(Role).all()

    result = []
    for role in roles:
        result.append({
            "id": role.id,
            "name": role.name,
            "permissions": [p.name for p in role.permissions]
        })

    return result

@router.put(
    "/users/{user_id}/role/{role_id}",
    dependencies=[Depends(require_permission("assign_role"))]
)
def assign_role(user_id: int, role_id: int, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.id == user_id).first()
    role = db.query(Role).filter(Role.id == role_id).first()

    if not user or not role:
        raise HTTPException(status_code=404, detail="User or role not found")

    user.role_id = role.id
    db.commit()

    return {"message": "Role assigned successfully"}

@router.get(
    "/users",
    dependencies=[Depends(require_permission("create_user"))]
)
def get_users(db: Session = Depends(get_db)):

    users = db.query(User).all()

    return [
        {
            "id": u.id,
            "email": u.email,
            "role": u.role.name if u.role else None
        }
        for u in users
    ]