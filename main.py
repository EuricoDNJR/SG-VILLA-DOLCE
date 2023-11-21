from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"api-version": "0.1.0"}