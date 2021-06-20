from fastapi import APIRouter
import requests

from ..utils import logging

router = APIRouter(route_class=logging.LoggingContextRoute)

url = 'https://jsonplaceholder.typicode.com/albums/'
response = requests.get(url)
status_code = response.status_code
albums = response.json()


@router.get("/")
async def read_albums():
    return {
        "status_code": status_code,
        "albums": albums,
    }
