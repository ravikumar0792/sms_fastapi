from fastapi import APIRouter, Depends, HTTPException
from jose import JWTError, jwt
import secrets
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app import db
from app.schemas.user import UserCreate, UserOut
from app.models.user import User
from app.models.role import Role
from app.db.deps import get_db
from app.core.security import hash_password
from fastapi.security import OAuth2PasswordRequestForm
from app.core.security import verify_password, create_access_token,create_refresh_token, create_password_reset_token
from app.core.config import settings
from app.core.dependencies import get_current_user
from app.core.email import send_verification_email, send_reset_email
from app.core.password_validator import validate_password_strength

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/signup", response_model=UserOut)
def signup(user: UserCreate, db: Session = Depends(get_db)):

    validate_password_strength(user.password)
    existing = db.query(User).filter(User.email == user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    db_role = db.query(Role).filter(Role.name == User.role_id).first()
    if not db_role:
        raise HTTPException(
            status_code=400, 
            detail=f"Role '{user.role_id}' does not exist."
        )
    token = secrets.token_urlsafe(32)
    expiry = datetime.utcnow() + timedelta(hours=24)

    new_user = User(
        first_name=user.first_name,
        last_name=user.last_name,
        phone=user.phone,
        email=user.email,
        hashed_password=hash_password(user.password),
        role=db_role,
        verification_token=token,
        verification_token_expiry=expiry,
        is_verified=False
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    send_verification_email(new_user.email, token)

    return new_user

@router.get("/verify")
def verify_email(token: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.verification_token == token).first()

    if not user:
        raise HTTPException(status_code=400, detail="Invalid token")

    user.is_verified = True
    user.verification_token = None
    user.verification_token_expiry = None
    db.commit()

    return {"message": "Email verified successfully"}

@router.post("/resend-verification")
def resend_verification(email: str, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.email == email).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user.is_verified:
        return {"message": "Email already verified"}

    token = secrets.token_urlsafe(32)
    expiry = datetime.utcnow() + timedelta(hours=24)

    user.verification_token = token
    user.verification_token_expiry = expiry
    db.commit()

    send_verification_email(user.email, token)

    return {"message": "Verification email sent"}

@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == form_data.username).first()

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if hasattr(user, "is_verified") and not user.is_verified:
        raise HTTPException(status_code=403, detail="Email not verified")

    # 3️ Create tokens
    access_token = create_access_token(user)
    refresh_token = create_refresh_token(user)

    # 4️ Store refresh token (token rotation base)
    user.refresh_token = refresh_token
    db.commit()

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "role": user.role_id
    }

@router.post("/refresh")
def refresh_token(refresh_token: str, db: Session = Depends(get_db)):

    try:
        payload = jwt.decode(
            refresh_token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )

        if payload.get("type") != "refresh":
            raise HTTPException(status_code=401, detail="Invalid token type")

        email = payload.get("sub")

    except:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    user = db.query(User).filter(User.email == email).first()

    if not user or user.refresh_token != refresh_token:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    # Token rotation
    new_access_token = create_access_token(user)
    new_refresh_token = create_refresh_token(user)

    user.refresh_token = new_refresh_token
    db.commit()

    return {
        "access_token": new_access_token,
        "refresh_token": new_refresh_token
    }

@router.post("/logout")
def logout(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    
    current_user.refresh_token = None
    db.commit()

    return {"message": "Logged out successfully"}

@router.post("/forgot-password")
def forgot_password(email: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    token = create_password_reset_token(user.email)

    user.reset_token = token
    user.reset_token_expire = datetime.utcnow() + timedelta(minutes=15)
    db.commit()

    send_reset_email(user.email, token)

    return {"message": "Password reset email sent"}

@router.post("/reset-password")
def reset_password(token: str, new_password: str, db: Session = Depends(get_db)):

    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )

        if payload.get("type") != "reset":
            raise HTTPException(status_code=400, detail="Invalid token")

        email = payload.get("sub")

    except JWTError:
        raise HTTPException(status_code=400, detail="Invalid or expired token")

    user = db.query(User).filter(User.email == email).first()

    if not user or user.reset_token != token:
        raise HTTPException(status_code=400, detail="Invalid token")
    validate_password_strength(new_password)
    user.hashed_password = hash_password(new_password)
    user.reset_token = None
    user.reset_token_expire = None
    db.commit()

    return {"message": "Password reset successful"}