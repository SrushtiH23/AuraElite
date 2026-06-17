"""
FastAPI dependency injection helpers.
- get_db: yields a database session
- get_current_user: validates JWT and returns the authenticated User
"""

from typing import Generator

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.session import SessionLocal
from app.models.user import User
from app.schemas.user import TokenPayload

# OAuth2 scheme — tells FastAPI to look for a Bearer token in the
# Authorization header. tokenUrl points at the login endpoint.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


# ── Database Session Dependency ──────────────────────────────────


def get_db() -> Generator:
    """Yield a SQLAlchemy session and close it when the request ends."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ── Current User Dependency (Route Protection) ──────────────────


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    """
    Decode and validate the JWT token from the Authorization header.
    Returns the corresponding User row or raises 401.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        token_data = TokenPayload(**payload)

        if token_data.sub is None:
            print("[DEBUG DEPS] sub is None", flush=True)
            raise credentials_exception
    except JWTError as je:
        print(f"[DEBUG DEPS] JWTError: {je}", flush=True)
        raise credentials_exception
    except Exception as ex:
        print(f"[DEBUG DEPS] General Exception: {ex}", flush=True)
        raise credentials_exception

    user = db.query(User).filter(User.id == token_data.sub).first()


    if user is None:
        print(f"[DEBUG DEPS] user not found in db for sub={token_data.sub}", flush=True)
        raise credentials_exception
    if not user.is_active:
        print(f"[DEBUG DEPS] user is inactive for sub={token_data.sub}", flush=True)
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user account",
        )

    return user
