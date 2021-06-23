from pydantic import BaseModel, Field
from typing import Optional

from ..docs.schemas import comment as docs_schemas_comment


class Comment(BaseModel):
    postId: int = Field(
        ...,
        title="投稿ID",
    )
    name: str = Field(
        ...,
        title="名前",
        min_length=1,
        max_length=100,
    )
    email: str = Field(
        ...,
        title="メールアドレス",
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
        schema_extra = docs_schemas_comment.Comment
