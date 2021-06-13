from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def root():
    return {"message": "v1 root"}
