from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.core.auth import verify_password, create_access_token, get_db
from app.schemas import TokenResponse
from app.models import User

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login", response_model=TokenResponse)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.login == form_data.username).first()
    if not user or not verify_password(
        form_data.password, user.hashed_password
    ):
        raise HTTPException(status_code=401, detail="Неверные учетные данные")

    token = create_access_token(data={"sub": user.username})
    return TokenResponse(access_token=token)
