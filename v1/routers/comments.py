from fastapi import APIRouter
import requests

from ..utils import logging

router = APIRouter(route_class=logging.LoggingContextRoute)

url = 'https://jsonplaceholder.typicode.com/comments/'
response = requests.get(url)
status_code = response.status_code
comments = response.json()


@router.get("/")
async def read_comments():
    return {
        "status_code": status_code,
        "comments": comments,
    }
