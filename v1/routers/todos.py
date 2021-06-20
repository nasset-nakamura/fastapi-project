from fastapi import APIRouter
import requests

from ..utils import logging

router = APIRouter(route_class=logging.LoggingContextRoute)

url = 'https://jsonplaceholder.typicode.com/todos/'
response = requests.get(url)
status_code = response.status_code
todos = response.json()


@router.get("/")
async def read_todos():
    return {
        "status_code": status_code,
        "todos": todos,
    }
