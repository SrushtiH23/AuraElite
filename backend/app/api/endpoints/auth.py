"""
Authentication API endpoints.

Routes:
    POST /api/auth/register  — Create a new user account
    POST /api/auth/login     — Authenticate and receive JWT
    GET  /api/auth/me        — Return the current authenticated user (protected)
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.core.security import create_access_token, get_password_hash, verify_password
from app.models.user import User
from app.schemas.user import Token, UserCreate, UserOut

router = APIRouter(prefix="/api/auth", tags=["Authentication"])


# ── POST /register ───────────────────────────────────────────────


@router.post(
    "/register",
    response_model=UserOut,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
)
def register(payload: UserCreate, db: Session = Depends(get_db)):
    """
    Create a new user account.

    - Validates that the email is not already taken.
    - Hashes the password before storing.
    - Returns the created user (without password).
    """
    # Check for existing user
    existing = db.query(User).filter(User.email == payload.email).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A user with this email already exists.",
        )

    user = User(
        email=payload.email,
        hashed_password=get_password_hash(payload.password),
        full_name=payload.full_name,
        is_active=True,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    return user


# ── POST /login ──────────────────────────────────────────────────


@router.post(
    "/login",
    response_model=Token,
    summary="Login and obtain access token",
)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    """
    Authenticate with email (username field) + password.

    Returns a JWT access token on success, or 401 on failure.
    """
    user = db.query(User).filter(User.email == form_data.username).first()

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This account has been deactivated.",
        )

    access_token = create_access_token(data={"sub": user.id})

    return Token(access_token=access_token)


# ── GET /me (Protected) ─────────────────────────────────────────


@router.get(
    "/me",
    response_model=UserOut,
    summary="Get current authenticated user",
)
def read_current_user(current_user: User = Depends(get_current_user)):
    """
    Returns the profile of the currently authenticated user.
    Requires a valid Bearer token in the Authorization header.
    """
    return current_user
