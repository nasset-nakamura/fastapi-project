import math

from fastapi import APIRouter, Body, Path, Query, Response, status, HTTPException
from fastapi.responses import JSONResponse
import requests
from typing import Optional

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
             }


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

    # key-value、row
    if fields:
        tmp_posts_2 = []
        for post in tmp_posts_1[offset:offset + limit]:
            tmp_post = {}
            for field in fields.split(","):
                if field in post:
                    tmp_post[field] = post[field]
                else:
                    response.status_code = status.HTTP_400_BAD_REQUEST
                    return {"message": f"field: {field} not found"}
            tmp_posts_2.append(tmp_post)
    else:
        tmp_posts_2 = tmp_posts_1[offset:offset + limit]

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

    headers = {
        "X-Users-Total-Count": str(count),
        "X-Users-Count": str(len(tmp_posts_3)),
        "X-Users-Max-Page": str(max_page),
        "X-Users-Current-Page": str(current_page),
    }
    content = tmp_posts_3

    return JSONResponse(headers=headers, content=content)
