from fastapi import Depends, HTTPException, status
from app.core.security import get_current_user


def require_permission(permission_name: str):

    def permission_checker(current_user=Depends(get_current_user)):
        if not current_user.role:
            raise HTTPException(status_code=403, detail="No role assigned")

        user_permissions = [p.name for p in current_user.role.permissions]

        if permission_name not in user_permissions:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions"
            )

        return current_user

    return permission_checker