from fastapi import Depends, FastAPI
from starlette.middleware.cors import CORSMiddleware

from config import config
from .docs import main as docs_main
from .routers import auth, comments, others, posts, users
from .utils import auth as auth_util
from .utils import logging

app = FastAPI(
    title=config.api_title,
    version=config.api_version,
    description=docs_main.app["description"],
    openapi_tags=docs_main.app["tags_metadata"],
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(
    users.router,
    prefix="/users",
    tags=["users"],
    dependencies=[Depends(auth_util.get_current_active_user)]
)

app.include_router(
    posts.router,
    prefix="/posts",
    tags=["posts"],
    dependencies=[Depends(auth_util.get_current_active_user)]
)

app.include_router(
    comments.router,
    prefix="/comments",
    tags=["comments"],
    dependencies=[Depends(auth_util.get_current_active_user)]
)

app.include_router(
    auth.router,
    prefix="/auth",
    tags=["auth"],
)

app.include_router(
    others.router,
    prefix="/others",
    tags=["others"],
    dependencies=[Depends(auth_util.get_current_active_user)]
)

app.router.route_class = logging.LoggingContextRoute


@app.get(
    "/",
    summary=docs_main.root["summary"],
    responses=docs_main.root["responses"],
)
def root():
    return {
        "version": config.api_version,
    }
