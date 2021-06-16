from fastapi import APIRouter
import requests

router = APIRouter()

url = 'https://jsonplaceholder.typicode.com/photos/'
response = requests.get(url)
status_code = response.status_code
photos = response.json()


@router.get("/")
async def read_photos():
    return {
        "status_code": status_code,
        "photos": photos,
    }
