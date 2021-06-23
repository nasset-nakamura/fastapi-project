import math

from fastapi import APIRouter, Body, Path, Query, Response, status, HTTPException
from fastapi.responses import JSONResponse
import requests
from typing import Optional

from ..schemas.post import Post
from ..utils import logging

router = APIRouter(route_class=logging.LoggingContextRoute)

url = 'https://jsonplaceholder.typicode.com/posts/'
response = requests.get(url)
status_code = response.status_code
posts = response.json()

responses = {"get:/": {200: {"content": {"application/json": {"example": {"userId": 1,
                                                                          "id": 1,
                                                                          "title": "sunt aut facere repellat provident occaecati excepturi optio reprehenderit",
                                                                          "body": "quia et suscipit\nsuscipit recusandae consequuntur expedita et cum\nreprehenderit molestiae ut ut quas totam\nnostrum rerum est autem sunt rem eveniet architecto"},
                                                              },
                                         },
                             },
                       400: {"content": {"application/json": {"example": {"message": "field: xxx not found"},
                                                              },
                                         },
                             },
                       404: {"content": {"application/json": {"example": {"message": "post not found"},
                                                              },
                                         },
                             },
                       },
             "get:/id": {200: {"content": {"application/json": {"example": {"userId": 1,
                                                                            "id": 1,
                                                                            "title": "sunt aut facere repellat provident occaecati excepturi optio reprehenderit",
                                                                            "body": "quia et suscipit\nsuscipit recusandae consequuntur expedita et cum\nreprehenderit molestiae ut ut quas totam\nnostrum rerum est autem sunt rem eveniet architecto"},
                                                                },
                                           },
                               },
                         400: {"content": {"application/json": {"example": {"message": "field: xxx not found"},
                                                                },
                                           },
                               },
                         404: {"content": {"application/json": {"example": {"message": "post not found"},
                                                                },
                                           },
                               },
                         },
             "post:/": {201: {"content": {"application/json": {"example": {"id": 101,
                                                                           "name": "test",
                                                                           "title": "タイトル",
                                                                           "body": "あいうえおカキクケコ"},
                                                               },
                                          },
                              },
                        },
             "put:/id": {201: {"content": {"application/json": {"example": {"id": 101,
                                                                            "name": "test",
                                                                            "title": "タイトル",
                                                                            "body": "あいうえおカキクケコ"},
                                                                },
                                           },
                               },
                         409: {"content": {"application/json": {"example": {"message": f"id.99 already exists"},
                                                                },
                                           },
                               },
                         },
             "patch:/id": {200: {"content": {"application/json": {"example": {"userId": 1,
                                                                              "id": 1,
                                                                              "title": "sunt aut facere repellat provident occaecati excepturi optio reprehenderit",
                                                                              "body": "quia et suscipit\nsuscipit recusandae consequuntur expedita et cum\nreprehenderit molestiae ut ut quas totam\nnostrum rerum est autem sunt rem eveniet architecto"},
                                                                  },
                                             },
                                 },
                           404: {"content": {"application/json": {"example": {"message": "post not found"},
                                                                  },
                                             },
                                 },
                           },
             "delete:/id": {202: {"content": {"application/json": {"example": "nothing",
                                                                   },
                                              },
                                  },
                            404: {"content": {"application/json": {"example": {"message": "post not found"},
                                                                   },
                                              },
                                  },
                            }}


@router.get("/", summary="投稿のリストを取得する", responses=responses["get:/"])
async def read_posts(
    response: Response,
    size: int = Query(
        10,
        ge=1,
        le=100,
        description="1ページあたりの取得件数を指定する。",
    ),
    page: int = Query(
        1,
        ge=1,
        description="取得するページを指定する。",
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

    count = len(tmp_posts_1)

    max_page = math.ceil(count / size)
    if page is None:
        current_page = 1
    elif page > max_page:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": f"page: {page} not found"}
    else:
        current_page = page
    offset = size * (current_page - 1)
    limit = size * current_page

    # sort
    if orders:
        if orders[0] == "-":
            orders = orders[1:]
            if orders in tmp_posts_1[0]:
                tmp_posts_2 = sorted(
                    tmp_posts_1, key=lambda item: (
                        item[orders]), reverse=True)
            else:
                response.status_code = status.HTTP_400_BAD_REQUEST
                return {"message": f"field: {orders} not found"}
        else:
            if orders in tmp_posts_1[0]:
                tmp_posts_2 = sorted(
                    tmp_posts_1, key=lambda item: (
                        item[orders]))
            else:
                response.status_code = status.HTTP_400_BAD_REQUEST
                return {"message": f"field: {orders} not found"}
    else:
        tmp_posts_2 = tmp_posts_1

    # key-value、row
    if fields:
        tmp_posts_3 = []
        for post in tmp_posts_2[offset:offset + limit]:
            tmp_post = {}
            for field in fields.split(","):
                if field in post:
                    tmp_post[field] = post[field]
                else:
                    response.status_code = status.HTTP_400_BAD_REQUEST
                    return {"message": f"field: {field} not found"}
            tmp_posts_3.append(tmp_post)
    else:
        tmp_posts_3 = tmp_posts_2[offset:offset + limit]

    headers = {
        "X-Posts-Total-Count": str(count),
        "X-Posts-Count": str(len(tmp_posts_3)),
        "X-Posts-Max-Page": str(max_page),
        "X-Posts-Current-Page": str(current_page),
    }
    content = tmp_posts_3

    return JSONResponse(headers=headers, content=content)


@router.get("/{id}", summary="投稿を1件取得する", responses=responses["get:/id"])
async def read_post(
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


@router.post("/", status_code=status.HTTP_201_CREATED,
             summary="投稿を追加する", responses=responses["post:/"])
async def create_post(
    post: Post = Body(
        ...,
    ),
):
    id = max([post["id"] for post in posts]) + 1
    tmp_post = {"id": id, **post.dict()}
    posts.append(tmp_post)

    return tmp_post


@router.put("/{id}",
            status_code=status.HTTP_201_CREATED,
            summary="idを指定して投稿を追加する", responses=responses["put:/id"])
async def create_post_by_specifying_id(
    response: Response,
    id: int = Path(
        ...,
        ge=1,
        description="追加するデータのidを指定する。",
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


@router.patch("/{id}", summary="投稿を更新する", responses=responses["patch:/id"])
async def update_post(
    response: Response,
    id: int = Path(
        ...,
        ge=1,
        description="更新するデータのidを指定する。",
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
    summary="投稿を削除する",
    responses=responses["delete:/id"]
)
async def delete_post(
    response: Response,
    id: int = Path(
        ...,
        ge=1,
        description="削除するデータのidを指定する。",
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
