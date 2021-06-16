from fastapi import APIRouter
import requests

router = APIRouter()

url = 'https://jsonplaceholder.typicode.com/users/'
response = requests.get(url)
status_code = response.status_code
users = response.json()


@router.get("/")
async def read_users():
    return {
        "status_code": status_code,
        "users": users,
    }
