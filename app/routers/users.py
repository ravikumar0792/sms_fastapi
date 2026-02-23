from fastapi import APIRouter, Depends
from app.core.dependencies import get_current_user
from app.models.user import User
from app.schemas.user import UserOut

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/dashboard", response_model=UserOut)
def read_users_me(current_user=Depends(get_current_user)):
    return current_user