from datetime import datetime
import time

from fastapi import APIRouter, BackgroundTasks, Query, Request, Response

from ..utils import logging

router = APIRouter(route_class=logging.LoggingContextRoute)


def background_sleep(sleep):
    count = 0
    while count < sleep:
        time.sleep(1)
        count += 1

    print({
        "message": "background task end!",
        "datetime": datetime.now().strftime("%Y/%m/%d %H:%M:%S%Z"),
    })


@router.post("/background")
async def background(
    background_tasks: BackgroundTasks,
    sleep: int = Query(
        ...,
        ge=1,
        le=30,
    ),
):
    background_tasks.add_task(background_sleep, sleep)
    return {
        "message": "background task start!",
        "datetime": datetime.now().strftime("%Y/%m/%d %H:%M:%S%Z"),
    }


@router.get("/cookie")
async def read_cookies(request: Request):
    return {"test": request.cookies.get("test")}


@router.post("/cookie")
async def create_cookies(response: Response):
    response.set_cookie(key="test", value="fastapi cookie")
    return {"Save cookies with fastapi"}
