read_users = {
    "summary": "ユーザーのリストを取得する",
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
                "`equals`：条件に一致したデータを取得する。（例：`id[equals]2`）<br>"
                "`not_equals`：条件に一致しないデータを取得する。（例：`id[not_equals]2`）",
        },
        "embed": {
            "description": "投稿データを取得する場合はTrueを指定する。",
        },
    },
    "responses": {
        200: {
            "content": {
                "application/json": {
                    "example": {
                        "id": 1,
                        "name": "Leanne Graham",
                        "username": "Bret",
                        "email": "Sincere@april.biz",
                        "address": {
                            "street": "Kulas Light",
                            "suite": "Apt. 556",
                            "city": "Gwenborough",
                            "zipcode": "92998-3874",
                            "geo": {
                                "lat": "-37.3159",
                                "lng": "81.1496"
                            }
                        },
                        "phone": "1-770-736-8031 x56442",
                        "website": "hildegard.org",
                        "company": {
                            "name": "Romaguera-Crona",
                            "catchPhrase": "Multi-layered client-server neural-net",
                            "bs": "harness real-time e-markets"
                        },
                    },
                },
            },
        },
        400: {
            "content": {
                "application/json": {
                    "example": {"message": "field: xxx not found"},
                },
            },
        },
        404: {
            "content": {
                "application/json": {
                    "example": {"message": "user not found"},
                },
            },
        },
    },
}

read_user = {
    "summary": "ユーザーを1件取得する",
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
                        "id": 1,
                        "name": "Leanne Graham",
                        "username": "Bret",
                        "email": "Sincere@april.biz",
                        "address": {
                            "street": "Kulas Light",
                            "suite": "Apt. 556",
                            "city": "Gwenborough",
                            "zipcode": "92998-3874",
                            "geo": {
                                "lat": "-37.3159",
                                "lng": "81.1496"
                            }
                        },
                        "phone": "1-770-736-8031 x56442",
                        "website": "hildegard.org",
                        "company": {
                            "name": "Romaguera-Crona",
                            "catchPhrase": "Multi-layered client-server neural-net",
                            "bs": "harness real-time e-markets"
                        },
                    },
                },
            },
        },
        400: {
            "content": {
                "application/json": {
                    "example": {"message": "field: xxx not found"},
                },
            },
        },
        404: {
            "content": {
                "application/json": {
                    "example": {"message": "user not found"},
                },
            },
        },
    },
}

create_user = {
    "summary": "ユーザーを追加する",
    "responses": {
        201: {
            "content": {
                "application/json": {
                    "example": {
                        "id": 11,
                        "name": "test",
                        "username": "testuser",
                        "email": "test@example.com"
                    },
                },
            },
        },
    },
}

create_user_by_specifying_id = {
    "summary": "idを指定してユーザーを追加する",
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
                        "id": 11,
                        "name": "test",
                        "username": "testuser",
                        "email": "test@example.com"
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

update_user = {
    "summary": "ユーザーを更新する",
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
                        "id": 1,
                        "name": "test",
                        "username": "testuser",
                        "email": "test@example.com",
                        "address": {
                            "street": "Kulas Light",
                            "suite": "Apt. 556",
                            "city": "Gwenborough",
                            "zipcode": "92998-3874",
                            "geo": {
                                "lat": "-37.3159",
                                "lng": "81.1496"
                            }
                        },
                        "phone": "1-770-736-8031 x56442",
                        "website": "hildegard.org",
                        "company": {
                            "name": "Romaguera-Crona",
                            "catchPhrase": "Multi-layered client-server neural-net",
                            "bs": "harness real-time e-markets"
                        },
                    },
                },
            },
        },
        404: {
            "content": {
                "application/json": {
                    "example": {"message": "user not found"},
                },
            },
        },
    },
}

delete_user = {
    "summary": "ユーザーを削除する",
    "parameters": {
        "id": {
            "description": "更新するデータのidを指定する。",
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
                    "example": {"message": "user not found"},
                },
            },
        },
    },
}
