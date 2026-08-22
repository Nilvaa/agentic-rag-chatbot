import jwt

from fastapi import Depends,HTTPException,status
from fastapi.security import HTTPBearer,HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.user import User
from app.services.auth_service import SECRET_KEY,ALGORITHM

security=HTTPBearer()

def get_db():
    db=SessionLocal()

    try:
        yield db
    finally:
        db.close()

def get_current_user(
        credentials:HTTPAuthorizationCredentials=Depends(security),
        db:Session=Depends(get_db)
):
    token=credentials.credentials

    try:
        payload=jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        user_id=payload.get("sub")

        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="invalid token"
            )

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="token expired"
        )

    except jwt.InvalidTokenError:
        raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="invalid token"
                )

    user=(
        db.query(User)
        .filter(User.id==int(user_id))
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    return user