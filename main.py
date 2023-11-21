from fastapi import FastAPI
import logging

logging.basicConfig(level=logging.INFO, filename='app.log', filemode='w', format="%(asctime)s - %(levelname)s - %(message)s")

app = FastAPI()

@app.get("/")
def read_root():
    logging.info("root")
    return {"api-version": "0.1.0"}