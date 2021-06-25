import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from config import config
from v1.main import app as v1_app

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

app.mount("/v1", v1_app)


@app.on_event("startup")
async def startup_event():
    print("■■■ Startup FastAPI!!! ■■■")


@app.on_event("shutdown")
async def shutdown_event():
    print("■■■ Shutdown FastAPI!!! ■■■")


@app.get("/")
def root():
    return {"message": "main root"}


if __name__ == "__main__":
    uvicorn.run(app, host=config.fastapi_url, port=config.fastapi_port)
