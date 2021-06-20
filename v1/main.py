from fastapi import Depends, FastAPI
from starlette.middleware.cors import CORSMiddleware

from .routers import albums, auth, comments, others, photos, posts, todos, users
from .utils import auth as auth_util
from .utils import logging

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(
    albums.router,
    prefix="/albums",
    tags=["albums"],
)

app.include_router(
    auth.router,
    prefix="/auth",
    tags=["auth"],
)

app.include_router(
    comments.router,
    prefix="/comments",
    tags=["comments"],
)

app.include_router(
    others.router,
    prefix="/others",
    tags=["others"],
)

app.include_router(
    photos.router,
    prefix="/photos",
    tags=["photos"],
)

app.include_router(
    posts.router,
    prefix="/posts",
    tags=["posts"],
)

app.include_router(
    todos.router,
    prefix="/todos",
    tags=["todos"],
)

app.include_router(
    users.router,
    prefix="/users",
    tags=["users"],
    dependencies=[Depends(auth_util.get_current_active_user)]
)

app.router.route_class = logging.LoggingContextRoute


@app.get("/", dependencies=[Depends(auth_util.get_current_active_user)])
def root():
    return {"message": "v1 root"}
