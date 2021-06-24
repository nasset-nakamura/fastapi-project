import math

from fastapi import APIRouter, Body, Path, Query, Response, status, HTTPException
from fastapi.responses import JSONResponse
import requests
from typing import Optional

from ..docs.routers import comments as docs_routers_comments
from ..schemas.comment import Comment
from ..utils import condition, logging

router = APIRouter(route_class=logging.LoggingContextRoute)

url = 'https://jsonplaceholder.typicode.com/comments/'
response = requests.get(url)
status_code = response.status_code
comments = response.json()


@router.get(
    "/",
    summary=docs_routers_comments.read_comments["summary"],
    responses=docs_routers_comments.read_comments["responses"],
)
async def read_comments(
    response: Response,
    size: int = Query(
        10,
        ge=1,
        le=100,
        description=docs_routers_comments.read_comments["parameters"]["size"]["description"],
    ),
    page: int = Query(
        1,
        ge=1,
        description=docs_routers_comments.read_comments["parameters"]["page"]["description"],
    ),
    ids: Optional[str] = Query(
        None,
        description=docs_routers_comments.read_comments["parameters"]["ids"]["description"],
    ),
    fields: Optional[str] = Query(
        None,
        description=docs_routers_comments.read_comments["parameters"]["fields"]["description"],
    ),
    orders: Optional[str] = Query(
        None,
        description=docs_routers_comments.read_comments["parameters"]["orders"]["description"],
    ),
    filters: Optional[str] = Query(
        None,
        description=docs_routers_comments.read_comments["parameters"]["filters"]["description"],
    ),
):
    # id
    if ids:
        tmp_comments_1 = []
        for id in ids.split(","):
            for comment in comments:
                if comment["id"] == int(id):
                    tmp_comments_1.append(comment)
    else:
        tmp_comments_1 = comments

    if len(tmp_comments_1) == 0:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"message": "comment not found"}

    # filters
    if filters:
        filter = condition.get_condition(filters)

        if filter["key"] not in tmp_comments_1[0]:
            response.status_code = status.HTTP_400_BAD_REQUEST
            return {"message": f"field: {filter['key']} not found"}

        if filter["condition"] == "equals":
            tmp_comments_2 = []
            for comment in tmp_comments_1:
                if isinstance(comment[filter["key"]], int):
                    if comment[filter["key"]] == int(filter["value"]):
                        tmp_comments_2.append(comment)
                elif isinstance(comment[filter["key"]], str):
                    if comment[filter["key"]] == filter["value"]:
                        tmp_comments_2.append(comment)

        elif filter["condition"] == "not_equals":
            tmp_comments_2 = []
            for comment in tmp_comments_1:
                if isinstance(comment[filter["key"]], int):
                    if comment[filter["key"]] != int(filter["value"]):
                        tmp_comments_2.append(comment)
                elif isinstance(comment[filter["key"]], str):
                    if comment[filter["key"]] != filter["value"]:
                        tmp_comments_2.append(comment)

        else:
            response.status_code = status.HTTP_400_BAD_REQUEST
            return {"message": f"condition: {filter['condition']} not found"}

    else:
        tmp_comments_2 = tmp_comments_1

    count = len(tmp_comments_2)

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
            if orders in tmp_comments_2[0]:
                tmp_comments_3 = sorted(
                    tmp_comments_2, key=lambda item: (
                        item[orders]), reverse=True)
            else:
                response.status_code = status.HTTP_400_BAD_REQUEST
                return {"message": f"field: {orders} not found"}
        else:
            if orders in tmp_comments_2[0]:
                tmp_comments_3 = sorted(
                    tmp_comments_2, key=lambda item: (
                        item[orders]))
            else:
                response.status_code = status.HTTP_400_BAD_REQUEST
                return {"message": f"field: {orders} not found"}
    else:
        tmp_comments_3 = tmp_comments_2

    # key-value、row
    if fields:
        tmp_comments_4 = []
        for comment in tmp_comments_3[offset:offset + size]:
            tmp_comment = {}
            for field in fields.split(","):
                if field in comment:
                    tmp_comment[field] = comment[field]
                else:
                    response.status_code = status.HTTP_400_BAD_REQUEST
                    return {"message": f"field: {field} not found"}
            tmp_comments_4.append(tmp_comment)
    else:
        tmp_comments_4 = tmp_comments_3[offset:offset + size]

    headers = {
        "X-Comments-Total-Count": str(count),
        "X-Comments-Count": str(len(tmp_comments_4)),
        "X-Comments-Max-Page": str(max_page),
        "X-Comments-Current-Page": str(current_page),
    }
    content = tmp_comments_4

    return JSONResponse(headers=headers, content=content)


@router.get(
    "/{id}",
    summary=docs_routers_comments.read_comment["summary"],
    responses=docs_routers_comments.read_comment["responses"],
)
async def read_comment(
    id: int = Path(
        ...,
        ge=1,
        description=docs_routers_comments.read_comment["parameters"]["id"]["description"],
    ),
    fields: Optional[str] = Query(
        None,
        description=docs_routers_comments.read_comment["parameters"]["fields"]["description"],
    ),
):
    # id
    tmp_comment_1 = None
    for comment in comments:
        if comment["id"] == id:
            tmp_comment_1 = comment
            break

    if tmp_comment_1 is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="comment not found")

    # key-value
    if fields:
        tmp_comment_2 = {}
        for field in fields.split(","):
            if field in tmp_comment_1:
                tmp_comment_2[field] = tmp_comment_1[field]
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"field: {field} not found")
    else:
        tmp_comment_2 = tmp_comment_1

    return tmp_comment_2


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    summary=docs_routers_comments.create_comment["summary"],
    responses=docs_routers_comments.create_comment["responses"],
)
async def create_comment(
    comment: Comment = Body(
        ...,
    ),
):
    id = max([comment["id"] for comment in comments]) + 1
    tmp_comment = {"id": id, **comment.dict()}
    comments.append(tmp_comment)

    return tmp_comment


@router.put("/{id}",
            status_code=status.HTTP_201_CREATED,
            summary=docs_routers_comments.create_comment_by_specifying_id["summary"],
            responses=docs_routers_comments.create_comment_by_specifying_id["responses"],
            )
async def create_comment_by_specifying_id(
    response: Response,
    id: int = Path(
        ...,
        ge=1,
        description=docs_routers_comments.create_comment_by_specifying_id["parameters"]["id"]["description"],
    ),
    comment: Comment = Body(
        ...,
    ),
):
    for tmp_comment in comments:
        if tmp_comment["id"] == id:
            response.status_code = status.HTTP_409_CONFLICT
            return {"message": f"id.{id} already exists"}
    tmp_comment = {"id": id, **comment.dict()}
    comments.append(tmp_comment)

    return tmp_comment


@router.patch(
    "/{id}",
    summary=docs_routers_comments.update_comment["summary"],
    responses=docs_routers_comments.update_comment["responses"],
)
async def update_comment(
    response: Response,
    id: int = Path(
        ...,
        ge=1,
        description=docs_routers_comments.update_comment["parameters"]["id"]["description"],
    ),
    comment: Comment = Body(
        ...,
    ),
):
    index = None
    for i, tmp_comment in enumerate(comments):
        if tmp_comment["id"] == id:
            index = i
            break

    if index is None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"message": "comment not found"}
    else:
        comments[index].update(**comment.dict())

    return comments[index]


@router.delete(
    "/{id}",
    status_code=status.HTTP_202_ACCEPTED,
    summary=docs_routers_comments.delete_comment["summary"],
    responses=docs_routers_comments.delete_comment["responses"],
)
async def delete_comment(
    response: Response,
    id: int = Path(
        ...,
        ge=1,
        description=docs_routers_comments.delete_comment["parameters"]["id"]["description"],
    ),
):
    index = None
    for i, comment in enumerate(comments):
        if comment["id"] == id:
            index = i
            break

    if index is None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"message": "comment not found"}
    else:
        comments.pop(index)

    return
