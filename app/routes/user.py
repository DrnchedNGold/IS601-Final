from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.schemas.user import UserUpdate, PasswordUpdate, UserResponse
from app.auth.dependencies import get_current_user_db
from app.auth.jwt import get_password_hash

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

@router.get("/me", response_model=UserResponse)
def read_profile(current_user: User = Depends(get_current_user_db)):
    """Get current user's profile."""
    return current_user

@router.put("/me", response_model=UserResponse)
def update_profile(
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_db)
):
    """Update current user's profile info."""
    update_data = user_update.dict(exclude_unset=True)
    # Prevent updating email/username to existing ones
    if "email" in update_data:
        existing = db.query(User).filter(User.email == update_data["email"], User.id != current_user.id).first()
        if existing:
            raise HTTPException(status_code=400, detail="Email already in use")
    if "username" in update_data:
        existing = db.query(User).filter(User.username == update_data["username"], User.id != current_user.id).first()
        if existing:
            raise HTTPException(status_code=400, detail="Username already in use")
    for key, value in update_data.items():
        setattr(current_user, key, value)
    db.commit()
    db.refresh(current_user)
    return current_user

@router.post("/me/change-password", status_code=204)
def change_password(
    pw_update: PasswordUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_db)
):
    """Change current user's password."""
    if not current_user.verify_password(pw_update.current_password):
        raise HTTPException(status_code=400, detail="Current password is incorrect")
    current_user.password = get_password_hash(pw_update.new_password)
    db.commit()
    return
