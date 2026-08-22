from fastapi import APIRouter,Depends,HTTPException,status
from sqlalchemy.orm import Session
import bcrypt

from app.database import SessionLocal
from app.models.user import User
from app.schemas.auth import (RegisterRequest,LoginRequest,UserResponse,TokenResponse)
from app.auth.security import hashed_password
from app.services.auth_service import create_access_token   

router=APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

def get_db():
    db=SessionLocal()

    try:
        yield db
    finally:
        db.close()

@router.post("/register",response_model=UserResponse)
def register(
    request:RegisterRequest,
    db:Session=Depends(get_db)
):
    existing_user=(
        db.query(User)
        .filter(User.email==request.email)
        .first()
    )

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already exist"
        )

    password_hash=bcrypt.hashpw(
        request.password.encode("utf-8"),
        bcrypt.gensalt()
    ).decode("utf-8")

    user=User(
        email=request.email,
        password_hash=password_hash
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user

@router.post("/login",response_model=TokenResponse)
def login(
    request:LoginRequest,
    db: Session=Depends(get_db)
):
    user=(
        db.query(User)
        .filter(User.email==request.email)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid username/password"
        )

    password_valid=bcrypt.checkpw(
        request.password.encode("utf-8"),
        user.password_hash.encode("utf-8")
    )

    if not password_valid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid username/password"
        )

    access_token=create_access_token(user.id)
    return {
        "access_token":access_token,
        "token_type":"bearer"
    }