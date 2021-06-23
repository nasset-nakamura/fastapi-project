from pydantic import BaseModel, Field
from typing import Optional

from ..docs.schemas import user as docs_schemas_user


class User(BaseModel):
    name: str = Field(
        ...,
        title="名前",
        min_length=1,
        max_length=100,
    )
    username: Optional[str] = Field(
        None,
        title="ユーザー名",
        min_length=1,
        max_length=100,
    )
    email: str = Field(
        ...,
        title="メールアドレス",
        min_length=1,
        max_length=100,
    )

    class Config:
        schema_extra = docs_schemas_user.User


class UserDB(User):
    hashed_password: str = Field(
        ...,
        title="ハッシュ",
    ),
    disabled: Optional[bool] = Field(
        ...,
        title="無効",
    )
