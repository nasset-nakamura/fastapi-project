from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.security import OAuth2PasswordRequestForm

from ..schemas.auth import Token
from ..utils import auth
from ..utils import logging

router = APIRouter(route_class=logging.LoggingContextRoute)

responses = {
    "/password_hash": {
        200: {
            "content": {
                "application/json": {
                    "example": {
                        "password": "password",
                        "hash_password": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
                    },
                },
            },
        },
    },
}


@router.get("/password_hash", summary="ハッシュ暗号したパスワードを返却する",
            responses=responses["/password_hash"])
def get_password_hash(
    password: str = Query(
        ...,
        description="ハッシュ暗号するパスワードを指定する。",
    ),
):
    return {
        "password": password,
        "hash_password": auth.get_password_hash(password)
    }


@router.post("/token", response_model=Token, summary="アクセストークンを取得する")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = auth.authenticate_user(
        auth.fake_users_db,
        form_data.username,
        form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
