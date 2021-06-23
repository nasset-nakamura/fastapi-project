from pydantic import BaseModel, Field
from typing import Optional


class Post(BaseModel):
    userId: int = Field(
        ...,
        title="ユーザーID",
    )
    title: str = Field(
        ...,
        title="タイトル",
        min_length=1,
        max_length=100,
    )
    body: Optional[str] = Field(
        ...,
        title="本文",
        min_length=1,
        max_length=200,
    )

    class Config:
        schema_extra = {
            "example": {
                "userId": 1,
                "title": "タイトル",
                "body": "あいうえおカキクケコ",
            }
        }
