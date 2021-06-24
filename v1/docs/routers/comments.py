read_comments = {
    "summary": "コメントのリストを取得する",
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
                "`equals`：条件に一致したデータを取得する。（例：`postId[equals]2`）<br>"
                "`not_equals`：条件に一致しないデータを取得する。（例：`postId[not_equals]2`）",
        },
    },
    "responses": {
        200: {
            "content": {
                "application/json": {
                    "example": {
                        "postId": 1,
                        "id": 1,
                        "name": "id labore ex et quam laborum",
                        "email": "Eliseo@gardner.biz",
                        "body": "laudantium enim quasi est quidem magnam voluptate ipsam eos\ntempora quo necessitatibus\ndolor quam autem quasi\nreiciendis et nam sapiente accusantium"
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
                        "message": "comment not found"
                    },
                },
            },
        },
    },
}

read_comment = {
    "summary": "コメントを1件取得する",
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
                        "postId": 1,
                        "id": 1,
                        "name": "id labore ex et quam laborum",
                        "email": "Eliseo@gardner.biz",
                        "body": "laudantium enim quasi est quidem magnam voluptate ipsam eos\ntempora quo necessitatibus\ndolor quam autem quasi\nreiciendis et nam sapiente accusantium"
                    }
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
                        "message": "comment not found"
                    },
                },
            },
        },
    },
}

create_comment = {
    "summary": "コメントを追加する",
    "responses": {
        201: {
            "content": {
                "application/json": {
                    "example": {
                        "id": 501,
                        "postId": 501,
                        "name": "commentuser",
                        "email": "comment@example.com",
                        "body": "あいうえおカキクケコ"
                    },
                },
            },
        },
    },
}

create_comment_by_specifying_id = {
    "summary": "idを指定してコメントを追加する",
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
                        "id": 501,
                        "postId": 501,
                        "name": "commentuser",
                        "email": "comment@example.com",
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

update_comment = {
    "summary": "コメントを更新する",
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
                        "id": 501,
                        "postId": 501,
                        "name": "commentuser",
                        "email": "comment@example.com",
                        "body": "あいうえおカキクケコ"
                    },
                },
            },
        },
        404: {
            "content": {
                "application/json": {
                    "example": {
                        "message": "comment not found"
                    },
                },
            },
        },
    },
}

delete_comment = {
    "summary": "コメントを削除する",
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
                        "message": "comment not found"
                    },
                },
            },
        },
    },
}
