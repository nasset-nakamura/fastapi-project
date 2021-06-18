from fastapi import APIRouter, Body, Path, Query
import requests
from typing import Optional

from ..schemas.user import User


router = APIRouter()

url = 'https://jsonplaceholder.typicode.com/users/'
response = requests.get(url)
status_code = response.status_code
users = response.json()


@router.get("/")
async def read_users(
    offset: int = Query(
        0,
        ge=0,
        description="何件目から取得するかを指定する。<br>`limit`パラメータと組み合わせてページング処理が可能。",
    ),
    limit: int = Query(
        10,
        ge=0,
        le=30,
        description="取得件数を指定する。<br>`offset`パラメータと組み合わせてページング処理が可能。",
    ),
    ids: Optional[str] = Query(
        None,
        description="取得するデータのidを`1,2,3`のようにカンマ区切りで指定する。",
    ),
    fields: Optional[str] = Query(
        None,
        description="取得するデータのフィールドを`id,name,email`のようにカンマ区切りで指定する。",
    ),
    orders: Optional[str] = Query(
        None,
        description="取得するデータの並べ替えを行う。<br>指定可能なフィールドは**1つのみ**。<br>降順は`-id`のように、フィールド名の先頭に`- (マイナス)`を付与。",
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

    # key-value、row
    if fields:
        tmp_users_2 = []
        for user in tmp_users_1[offset:offset + limit]:
            tmp_user = {}
            for field in fields.split(","):
                if field in user:
                    tmp_user[field] = user[field]
            tmp_users_2.append(tmp_user)
    else:
        tmp_users_2 = tmp_users_1[offset:offset + limit]

    # sort
    if orders:
        if orders[0] == "-":
            orders = orders[1:]
            tmp_users_3 = sorted(
                tmp_users_2, key=lambda item: (
                    item[orders]), reverse=True)
        else:
            tmp_users_3 = sorted(
                tmp_users_2, key=lambda item: (
                    item[orders]))
    else:
        tmp_users_3 = tmp_users_2

    return {
        "status_code": status_code,
        "users": tmp_users_3,
    }


@router.get("/{id}")
async def read_user(
    id: int = Path(
        ...,
        ge=1,
        description="取得するデータのidを指定する。",
    ),
    fields: Optional[str] = Query(
        None,
        description="取得するデータのフィールドを`id,name,email`のようにカンマ区切りで指定する。",
    ),
):
    # id
    for user in users:
        if user["id"] == int(id):
            tmp_user_1 = user
            break

    # key-value
    if fields:
        tmp_user_2 = {}
        for field in fields.split(","):
            if field in tmp_user_1:
                tmp_user_2[field] = tmp_user_1[field]
    else:
        tmp_user_2 = tmp_user_1

    return {
        "status_code": status_code,
        "user": tmp_user_2,
    }


@router.post("/")
async def create_user(
    user: User = Body(
        ...,
    ),
):
    id = max([user["id"] for user in users]) + 1
    tmp_user = {"id": id, **user.dict()}
    users.append(tmp_user)

    return {
        "status_code": 201,
        "user": tmp_user,
    }


@router.put("/{id}")
async def create_user_by_specifying_id(
    id: int = Path(
        ...,
        ge=1,
        description="追加するデータのidを指定する。",
    ),
    user: User = Body(
        ...,
    ),
):
    tmp_user = {"id": id, **user.dict()}
    users.append(tmp_user)

    return {
        "status_code": 201,
        "user": tmp_user,
    }


@router.patch("/{id}")
async def update_user(
    id: int = Path(
        ...,
        ge=1,
        description="更新するデータのidを指定する。",
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

    if index >= 0:
        users[index].update(**user.dict())

    return {
        "status_code": 200,
        "user": users[index],
    }


@router.delete("/{id}")
async def delete_user(
    id: int = Path(
        ...,
        ge=1,
        description="削除するデータのidを指定する。",
    ),
):
    index = None
    for i, user in enumerate(users):
        if user["id"] == int(id):
            index = i
            break

    if index:
        users.pop(index)

    return {
        "status_code": 202,
    }
