import math

from fastapi import APIRouter, Body, Path, Query, Response, status, HTTPException
from fastapi.responses import JSONResponse
import requests
from typing import Optional

from ..docs.routers import posts as docs_routers_posts
from ..schemas.post import Post
from ..utils import condition, logging

router = APIRouter(route_class=logging.LoggingContextRoute)

url = 'https://jsonplaceholder.typicode.com/posts/'
response = requests.get(url)
status_code = response.status_code
posts = response.json()


@router.get(
    "/",
    summary=docs_routers_posts.read_posts["summary"],
    responses=docs_routers_posts.read_posts["responses"],
)
async def read_posts(
    response: Response,
    size: int = Query(
        10,
        ge=1,
        le=100,
        description=docs_routers_posts.read_posts["parameters"]["size"]["description"],
    ),
    page: int = Query(
        1,
        ge=1,
        description=docs_routers_posts.read_posts["parameters"]["page"]["description"],
    ),
    ids: Optional[str] = Query(
        None,
        description=docs_routers_posts.read_posts["parameters"]["ids"]["description"],
    ),
    fields: Optional[str] = Query(
        None,
        description=docs_routers_posts.read_posts["parameters"]["fields"]["description"],
    ),
    orders: Optional[str] = Query(
        None,
        description=docs_routers_posts.read_posts["parameters"]["orders"]["description"],
    ),
    filters: Optional[str] = Query(
        None,
        description=docs_routers_posts.read_posts["parameters"]["filters"]["description"],
    )
):
    # id
    if ids:
        tmp_posts_1 = []
        for id in ids.split(","):
            for post in posts:
                if post["id"] == int(id):
                    tmp_posts_1.append(post)
    else:
        tmp_posts_1 = posts

    if len(tmp_posts_1) == 0:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"message": "post not found"}

    # filters
    if filters:
        filter = condition.get_condition(filters)

        if filter["key"] not in tmp_posts_1[0]:
            response.status_code = status.HTTP_400_BAD_REQUEST
            return {"message": f"field: {filter['key']} not found"}

        if filter["condition"] == "equals":
            tmp_posts_2 = []
            for post in tmp_posts_1:
                if isinstance(post[filter["key"]], int):
                    if post[filter["key"]] == int(filter["value"]):
                        tmp_posts_2.append(post)
                elif isinstance(post[filter["key"]], str):
                    if post[filter["key"]] == filter["value"]:
                        tmp_posts_2.append(post)

        elif filter["condition"] == "not_equals":
            tmp_posts_2 = []
            for post in tmp_posts_1:
                if isinstance(post[filter["key"]], int):
                    if post[filter["key"]] != int(filter["value"]):
                        tmp_posts_2.append(post)
                elif isinstance(post[filter["key"]], str):
                    if post[filter["key"]] != filter["value"]:
                        tmp_posts_2.append(post)

        else:
            response.status_code = status.HTTP_400_BAD_REQUEST
            return {"message": f"condition: {filter['condition']} not found"}

    else:
        tmp_posts_2 = tmp_posts_1

    count = len(tmp_posts_2)

    max_page = math.ceil(count / size)
    if page is None:
        current_page = 1
    elif page > max_page:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": f"page: {page} not found"}
    else:
        current_page = page
    offset = size * (current_page - 1)

    # sort
    if orders:
        if orders[0] == "-":
            orders = orders[1:]
            if orders in tmp_posts_2[0]:
                tmp_posts_3 = sorted(
                    tmp_posts_2, key=lambda item: (
                        item[orders]), reverse=True)
            else:
                response.status_code = status.HTTP_400_BAD_REQUEST
                return {"message": f"field: {orders} not found"}
        else:
            if orders in tmp_posts_2[0]:
                tmp_posts_3 = sorted(
                    tmp_posts_2, key=lambda item: (
                        item[orders]))
            else:
                response.status_code = status.HTTP_400_BAD_REQUEST
                return {"message": f"field: {orders} not found"}
    else:
        tmp_posts_3 = tmp_posts_2

    # key-value、row
    if fields:
        tmp_posts_4 = []
        for post in tmp_posts_3[offset:offset + size]:
            tmp_post = {}
            for field in fields.split(","):
                if field in post:
                    tmp_post[field] = post[field]
                else:
                    response.status_code = status.HTTP_400_BAD_REQUEST
                    return {"message": f"field: {field} not found"}
            tmp_posts_4.append(tmp_post)
    else:
        tmp_posts_4 = tmp_posts_3[offset:offset + size]

    headers = {
        "X-Posts-Total-Count": str(count),
        "X-Posts-Count": str(len(tmp_posts_4)),
        "X-Posts-Max-Page": str(max_page),
        "X-Posts-Current-Page": str(current_page),
    }
    content = tmp_posts_4

    return JSONResponse(headers=headers, content=content)


@router.get(
    "/{id}",
    summary=docs_routers_posts.read_post["summary"],
    responses=docs_routers_posts.read_post["responses"],
)
async def read_post(
    id: int = Path(
        ...,
        ge=1,
        description=docs_routers_posts.read_post["parameters"]["id"]["description"],
    ),
    fields: Optional[str] = Query(
        None,
        description=docs_routers_posts.read_post["parameters"]["fields"]["description"],
    ),
):
    # id
    tmp_post_1 = None
    for post in posts:
        if post["id"] == id:
            tmp_post_1 = post
            break

    if tmp_post_1 is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="post not found")

    # key-value
    if fields:
        tmp_post_2 = {}
        for field in fields.split(","):
            if field in tmp_post_1:
                tmp_post_2[field] = tmp_post_1[field]
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"field: {field} not found")
    else:
        tmp_post_2 = tmp_post_1

    return tmp_post_2


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    summary=docs_routers_posts.create_post["summary"],
    responses=docs_routers_posts.create_post["responses"],
)
async def create_post(
    post: Post = Body(
        ...,
    ),
):
    id = max([post["id"] for post in posts]) + 1
    tmp_post = {"id": id, **post.dict()}
    posts.append(tmp_post)

    return tmp_post


@router.put(
    "/{id}",
    status_code=status.HTTP_201_CREATED,
    summary=docs_routers_posts.create_post_by_specifying_id["summary"],
    responses=docs_routers_posts.create_post_by_specifying_id["responses"],
)
async def create_post_by_specifying_id(
    response: Response,
    id: int = Path(
        ...,
        ge=1,
        description=docs_routers_posts.create_post_by_specifying_id["parameters"]["id"]["description"],
    ),
    post: Post = Body(
        ...,
    ),
):
    for tmp_post in posts:
        if tmp_post["id"] == id:
            response.status_code = status.HTTP_409_CONFLICT
            return {"message": f"id.{id} already exists"}
    tmp_post = {"id": id, **post.dict()}
    posts.append(tmp_post)

    return tmp_post


@router.patch(
    "/{id}",
    summary=docs_routers_posts.update_post["summary"],
    responses=docs_routers_posts.update_post["responses"],
)
async def update_post(
    response: Response,
    id: int = Path(
        ...,
        ge=1,
        description=docs_routers_posts.update_post["parameters"]["id"]["description"],
    ),
    post: Post = Body(
        ...,
    ),
):
    index = None
    for i, tmp_post in enumerate(posts):
        if tmp_post["id"] == id:
            index = i
            break

    if index is None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"message": "post not found"}
    else:
        posts[index].update(**post.dict())

    return posts[index]


@router.delete(
    "/{id}",
    status_code=status.HTTP_202_ACCEPTED,
    summary=docs_routers_posts.delete_post["summary"],
    responses=docs_routers_posts.delete_post["responses"],
)
async def delete_post(
    response: Response,
    id: int = Path(
        ...,
        ge=1,
        description=docs_routers_posts.delete_post["parameters"]["id"]["description"],
    ),
):
    index = None
    for i, post in enumerate(posts):
        if post["id"] == id:
            index = i
            break

    if index is None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"message": "post not found"}
    else:
        posts.pop(index)

    return
