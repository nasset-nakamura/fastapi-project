import math

from fastapi import APIRouter, Body, Path, Query, Response, status, HTTPException
from fastapi.responses import JSONResponse
import requests
from typing import Optional

from ..docs.routers import users as docs_routers_users
from ..schemas.user import User
from ..utils import logging

router = APIRouter(route_class=logging.LoggingContextRoute)

url = 'https://jsonplaceholder.typicode.com/users/'
res = requests.get(url)
status_code = res.status_code
users = res.json()


@router.get(
    "/",
    summary=docs_routers_users.read_users["summary"],
    responses=docs_routers_users.read_users["responses"],
)
async def read_users(
    response: Response,
    size: int = Query(
        10,
        ge=1,
        le=100,
        description=docs_routers_users.read_users["parameters"]["size"]["description"],
    ),
    page: int = Query(
        1,
        ge=1,
        description=docs_routers_users.read_users["parameters"]["page"]["description"],
    ),
    ids: Optional[str] = Query(
        None,
        description=docs_routers_users.read_users["parameters"]["ids"]["description"],
    ),
    fields: Optional[str] = Query(
        None,
        description=docs_routers_users.read_users["parameters"]["fields"]["description"],
    ),
    orders: Optional[str] = Query(
        None,
        description=docs_routers_users.read_users["parameters"]["orders"]["description"],
    ),
):
    # id
    if ids:
        tmp_users_1 = []
        for id in ids.split(","):
            for user in users:
                if user["id"] == int(id):
                    tmp_users_1.append(user)
    else:
        tmp_users_1 = users

    if len(tmp_users_1) == 0:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"message": "user not found"}

    count = len(tmp_users_1)

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
            if orders in tmp_users_1[0]:
                tmp_users_2 = sorted(
                    tmp_users_1, key=lambda item: (
                        item[orders]), reverse=True)
            else:
                response.status_code = status.HTTP_400_BAD_REQUEST
                return {"message": f"field: {orders} not found"}
        else:
            if orders in tmp_users_1[0]:
                tmp_users_2 = sorted(
                    tmp_users_1, key=lambda item: (
                        item[orders]))
            else:
                response.status_code = status.HTTP_400_BAD_REQUEST
                return {"message": f"field: {orders} not found"}
    else:
        tmp_users_2 = tmp_users_1

    # key-value、row
    if fields:
        tmp_users_3 = []
        for user in tmp_users_2[offset:offset + size]:
            tmp_user = {}
            for field in fields.split(","):
                if field in user:
                    tmp_user[field] = user[field]
                else:
                    response.status_code = status.HTTP_400_BAD_REQUEST
                    return {"message": f"field: {field} not found"}
            tmp_users_3.append(tmp_user)
    else:
        tmp_users_3 = tmp_users_2[offset:offset + size]

    headers = {
        "X-Users-Total-Count": str(count),
        "X-Users-Count": str(len(tmp_users_3)),
        "X-Users-Max-Page": str(max_page),
        "X-Users-Current-Page": str(current_page),
    }
    content = tmp_users_3

    return JSONResponse(headers=headers, content=content)


@router.get(
    "/{id}",
    summary=docs_routers_users.read_user["summary"],
    responses=docs_routers_users.read_user["responses"],
)
async def read_user(
    id: int = Path(
        ...,
        ge=1,
        description=docs_routers_users.read_user["parameters"]["id"]["description"],
    ),
    fields: Optional[str] = Query(
        None,
        description=docs_routers_users.read_user["parameters"]["fields"]["description"],
    ),
):
    # id
    tmp_user_1 = None
    for user in users:
        if user["id"] == id:
            tmp_user_1 = user
            break

    if tmp_user_1 is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="user not found")

    # key-value
    if fields:
        tmp_user_2 = {}
        for field in fields.split(","):
            if field in tmp_user_1:
                tmp_user_2[field] = tmp_user_1[field]
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"field: {field} not found")
    else:
        tmp_user_2 = tmp_user_1

    return tmp_user_2


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    summary=docs_routers_users.create_user["summary"],
    responses=docs_routers_users.create_user["responses"],
)
async def create_user(
    user: User = Body(
        ...,
    ),
):
    id = max([user["id"] for user in users]) + 1
    tmp_user = {"id": id, **user.dict()}
    users.append(tmp_user)

    return tmp_user


@router.put(
    "/{id}",
    status_code=status.HTTP_201_CREATED,
    summary=docs_routers_users.create_user_by_specifying_id["summary"],
    responses=docs_routers_users.create_user_by_specifying_id["responses"],
)
async def create_user_by_specifying_id(
    response: Response,
    id: int = Path(
        ...,
        ge=1,
        description=docs_routers_users.create_user_by_specifying_id["parameters"]["id"]["description"],
    ),
    user: User = Body(
        ...,
    ),
):
    for tmp_user in users:
        if tmp_user["id"] == id:
            response.status_code = status.HTTP_409_CONFLICT
            return {"message": f"id.{id} already exists"}
    tmp_user = {"id": id, **user.dict()}
    users.append(tmp_user)

    return tmp_user


@router.patch(
    "/{id}",
    summary=docs_routers_users.update_user["summary"],
    responses=docs_routers_users.update_user["responses"],
)
async def update_user(
    response: Response,
    id: int = Path(
        ...,
        ge=1,
        description=docs_routers_users.update_user["parameters"]["id"]["description"],
    ),
    user: User = Body(
        ...,
    ),
):
    index = None
    for i, tmp_user in enumerate(users):
        if tmp_user["id"] == id:
            index = i
            break

    if index is None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"message": "user not found"}
    else:
        users[index].update(**user.dict())

    return users[index]


@router.delete(
    "/{id}",
    status_code=status.HTTP_202_ACCEPTED,
    summary=docs_routers_users.delete_user["summary"],
    responses=docs_routers_users.delete_user["responses"],
)
async def delete_user(
    response: Response,
    id: int = Path(
        ...,
        ge=1,
        description=docs_routers_users.delete_user["parameters"]["id"]["description"],
    ),
):
    """
    # docstringの記載内容もOpenAPIに反映される

    ## 文字装飾

    **太字**<br>
    *斜体*<br>
    ~~取り消し線~~<br>
    文字色を<font color='red'>赤</font>に変更

    ---

    ## リスト

    - 番号なしリスト
    - 番号なしリスト
    - 番号なしリスト

    1. 番号ありリスト
    1. 番号ありリスト
    1. 番号ありリスト

    ---

    ## テーブル

    |左寄せ|中央寄せ|右寄せ|
    |:---|:---:|---:|
    |aaa|bbb|ccc|
    |ddd|eee|fff|

    ---

    ## コード

    `title`タグにページタイトルを記載

    ```
    def add(a, b):
        return a + b
    ```

    ---

    ## リンク

    [Google](https://google.com)
    """
    index = None
    for i, user in enumerate(users):
        if user["id"] == id:
            index = i
            break

    if index is None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"message": "user not found"}
    else:
        users.pop(index)

    return
