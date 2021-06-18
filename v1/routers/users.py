from fastapi import APIRouter
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
    offset: int = 0,
    limit: int = 10,
    ids: Optional[str] = None,
    fields: Optional[str] = None,
    orders: Optional[str] = None
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
    id: int,
    fields: Optional[str] = None,
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
async def create_user(user: User):
    id = max([user["id"] for user in users]) + 1
    tmp_user = {"id": id, **user.dict()}
    users.append(tmp_user)

    return {
        "status_code": 201,
        "user": tmp_user,
    }


@router.delete("/{id}")
async def delete_user(
    id: int,
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
