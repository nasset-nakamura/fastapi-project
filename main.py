import uvicorn
from fastapi import FastAPI

from config import config

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Hello World"}


if __name__ == "__main__":
    uvicorn.run(app, host=config.fastapi_url, port=config.fastapi_port)
