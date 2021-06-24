read_posts = {
    "summary": "投稿のリストを取得する",
    "parameters": {
        "size": {
            "description": "1ページあたりの取得件数を指定する。",
        },
        "page": {
            "description": "取得するページを指定する。",
        },
        "ids": {
            "description": "取得するデータのidを`1,2,3`のようにカンマ区切りで指定する。",
        },
        "fields": {
            "description": "取得するデータのフィールドを`id,name,email`のようにカンマ区切りで指定する。",
        },
        "orders": {
            "description":
                "取得するデータの並べ替えを行う。<br>"
                "指定可能なフィールドは**1つのみ**。<br>"
                "降順は`-id`のように、フィールド名の先頭に`- (マイナス)`を付与。",
        },
        "filters": {
            "description":
                "取得するデータの抽出条件を指定する。<br>"
                "`equals`：条件に一致したデータを取得する。（例：`userId[equals]2`）<br>"
                "`not_equals`：条件に一致しないデータを取得する。（例：`userId[not_equals]2`）",
        },
    },
    "responses": {
        200: {
            "content": {
                "application/json": {
                    "example": {
                        "userId": 1,
                        "id": 1,
                        "title": "sunt aut facere repellat provident occaecati excepturi optio reprehenderit",
                        "body": "quia et suscipit\nsuscipit recusandae consequuntur expedita et cum\nreprehenderit molestiae ut ut quas totam\nnostrum rerum est autem sunt rem eveniet architecto"
                    },
                },
            },
        },
        400: {
            "content": {
                "application/json": {
                    "example": {
                        "message": "field: xxx not found"
                    },
                },
            },
        },
        404: {
            "content": {
                "application/json": {
                    "example": {
                        "message": "post not found"
                    },
                },
            },
        },
    },
}

read_post = {
    "summary": "投稿を1件取得する",
    "parameters": {
        "id": {
            "description": "取得するデータのidを指定する。",
        },
        "fields": {
            "description": "取得するデータのフィールドを`id,name,email`のようにカンマ区切りで指定する。",
        },
    },
    "responses": {
        200: {
            "content": {
                "application/json": {
                    "example": {
                        "userId": 1,
                        "id": 1,
                        "title": "sunt aut facere repellat provident occaecati excepturi optio reprehenderit",
                        "body": "quia et suscipit\nsuscipit recusandae consequuntur expedita et cum\nreprehenderit molestiae ut ut quas totam\nnostrum rerum est autem sunt rem eveniet architecto"},
                },
            },
        },
        400: {
            "content": {
                "application/json": {
                    "example": {
                        "message": "field: xxx not found"
                    },
                },
            },
        },
        404: {
            "content": {
                "application/json": {
                    "example": {
                        "message": "post not found"
                    },
                },
            },
        },
    },
}

create_post = {
    "summary": "投稿を追加する",
    "responses": {
        201: {
            "content": {
                "application/json": {
                    "example": {
                        "id": 101,
                        "name": "test",
                        "title": "タイトル",
                        "body": "あいうえおカキクケコ"
                    },
                },
            },
        },
    },
}

create_post_by_specifying_id = {
    "summary": "idを指定して投稿を追加する",
    "parameters": {
        "id": {
            "description": "追加するデータのidを指定する。",
        },
    },
    "responses": {
        201: {
            "content": {
                "application/json": {
                    "example": {
                        "id": 101,
                        "name": "test",
                        "title": "タイトル",
                        "body": "あいうえおカキクケコ"
                    },
                },
            },
        },
        409: {
            "content": {
                "application/json": {
                    "example": {
                        "message": "id.99 already exists"
                    },
                },
            },
        },
    },
}

update_post = {
    "summary": "投稿を更新する",
    "parameters": {
        "id": {
            "description": "更新するデータのidを指定する。",
        },
    },
    "responses": {
        200: {
            "content": {
                "application/json": {
                    "example": {
                        "userId": 1,
                        "id": 1,
                        "title": "sunt aut facere repellat provident occaecati excepturi optio reprehenderit",
                        "body": "quia et suscipit\nsuscipit recusandae consequuntur expedita et cum\nreprehenderit molestiae ut ut quas totam\nnostrum rerum est autem sunt rem eveniet architecto"
                    },
                },
            },
        },
        404: {
            "content": {
                "application/json": {
                    "example": {
                        "message": "post not found"
                    },
                },
            },
        },
    },
}

delete_post = {
    "summary": "投稿を削除する",
    "parameters": {
        "id": {
            "description": "削除するデータのidを指定する。",
        },
    },
    "responses": {
        202: {
            "content": {
                "application/json": {
                    "example": "nothing",
                },
            },
        },
        404: {
            "content": {
                "application/json": {
                    "example": {
                        "message": "post not found"
                    },
                },
            },
        },
    },
}
