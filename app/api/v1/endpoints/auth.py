from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import create_access_token, verify_password
from app.models.user import User
from app.schemas.token import Token

router = APIRouter()

@router.post("/login", response_model=Token)
def login_access_token(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests.
    """
    print(f"DEBUG: Login attempt for username: '{form_data.username}'")
    print(f"DEBUG: Password received: '{form_data.password}'")
    
    user = db.query(User).filter(User.username == form_data.username).first()
    
    if not user:
        print("DEBUG: User not found in DB")
    else:
        is_password_correct = verify_password(form_data.password, user.hashed_password)
        print(f"DEBUG: User found. Hash in DB: {user.hashed_password[:10]}...")
        print(f"DEBUG: Password match result: {is_password_correct}")
    
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")

    # 4. Bikin Access Token
    access_token = create_access_token(data={"sub": user.username, "id": user.id})
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
    }