from pydantic import BaseModel, Field
from typing import Optional

from ..docs.schemas import post as docs_schemas_post


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
        schema_extra = docs_schemas_post.Post
