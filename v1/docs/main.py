app = {
    "description": """
## FastAPI

Markdownで記載可能。

- high performance
- easy to learn
- fast to code
- ready for production
""",
    "tags_metadata": [
        {
            "name": "default",
            "description": "Default Endpoint",
        },
        {
            "name": "users",
            "description": "JSON Placeholder - Users Resource",
            "externalDocs": {
                "description": "URL",
                "url": "https://jsonplaceholder.typicode.com/users",
            },
        },
        {
            "name": "posts",
            "description": "JSON Placeholder - Posts Resource",
            "externalDocs": {
                "description": "URL",
                "url": "https://jsonplaceholder.typicode.com/posts",
            },
        },
        {
            "name": "comments",
            "description": "JSON Placeholder - Comments Resource",
            "externalDocs": {
                "description": "URL",
                "url": "https://jsonplaceholder.typicode.com/comments",
            },
        },
        {
            "name": "others",
            "description": "Other Endpoint",
        },
    ],
}

root = {
    "summary": "バージョン情報を取得する",
    "responses": {
        200: {
            "content": {
                "application/json": {
                    "example": {
                        "version": "1.0.0",
                    },
                },
            },
        },
    },
}
