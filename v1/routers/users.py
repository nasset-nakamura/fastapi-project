from fastapi import APIRouter, Body, Path, Query, Response, status, HTTPException
import requests
from typing import Optional

from ..schemas.user import User


router = APIRouter()

url = 'https://jsonplaceholder.typicode.com/users/'
res = requests.get(url)
status_code = res.status_code
users = res.json()


@router.get("/", summary="ユーザーのリストを取得する")
async def read_users(
    response: Response,
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

    if len(tmp_users_1) == 0:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"message": "user not found"}

    # key-value、row
    if fields:
        tmp_users_2 = []
        for user in tmp_users_1[offset:offset + limit]:
            tmp_user = {}
            for field in fields.split(","):
                if field in user:
                    tmp_user[field] = user[field]
                else:
                    response.status_code = status.HTTP_400_BAD_REQUEST
                    return {"message": f"field: {field} not found"}
            tmp_users_2.append(tmp_user)
    else:
        tmp_users_2 = tmp_users_1[offset:offset + limit]

    # sort
    if orders:
        if orders[0] == "-":
            orders = orders[1:]
            if orders in tmp_users_2[0]:
                tmp_users_3 = sorted(
                    tmp_users_2, key=lambda item: (
                        item[orders]), reverse=True)
            else:
                response.status_code = status.HTTP_400_BAD_REQUEST
                return {"message": f"field: {orders} not found"}
        else:
            if orders in tmp_users_2[0]:
                tmp_users_3 = sorted(
                    tmp_users_2, key=lambda item: (
                        item[orders]))
            else:
                response.status_code = status.HTTP_400_BAD_REQUEST
                return {"message": f"field: {orders} not found"}
    else:
        tmp_users_3 = tmp_users_2

    return tmp_users_3


@router.get("/{id}", summary="ユーザーを1件取得する")
async def read_user(
    response: Response,
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


@router.post("/", status_code=status.HTTP_201_CREATED, summary="ユーザーを追加する")
async def create_user(
    user: User = Body(
        ...,
    ),
):
    id = max([user["id"] for user in users]) + 1
    tmp_user = {"id": id, **user.dict()}
    users.append(tmp_user)

    return tmp_user


@router.put("/{id}",
            status_code=status.HTTP_201_CREATED,
            summary="idを指定してユーザーを追加する")
async def create_user_by_specifying_id(
    response: Response,
    id: int = Path(
        ...,
        ge=1,
        description="追加するデータのidを指定する。",
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


@router.patch("/{id}", summary="ユーザーを更新する")
async def update_user(
    response: Response,
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

    if index is None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"message": "user not found"}
    else:
        users[index].update(**user.dict())

    return users[index]


@router.delete(
    "/{id}",
    status_code=status.HTTP_202_ACCEPTED,
    summary="ユーザーを削除する",
)
async def delete_user(
    response: Response,
    id: int = Path(
        ...,
        ge=1,
        description="削除するデータのidを指定する。",
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
