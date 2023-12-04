from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database.dbmain import db
from .database.models import Usuario, Pagamento, Cliente, Caixa, Produto, Pedido
from .routers.v1 import cliente, usuario, produto
from contextlib import asynccontextmanager

import logging

logging.basicConfig(level=logging.INFO, filename='app.log', filemode='w', format="%(asctime)s - %(levelname)s - %(message)s")

@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.info("Startup")
    logging.info("Connecting Database")
    db.connect()
    logging.info("Creating Tables")
    db.create_tables([Usuario, Pagamento, Cliente, Caixa, Produto, Pedido], safe=True)
    logging.info("Tables Created")
    
    yield

    logging.info("Shutdown")
    logging.info("Disconnecting Database")
    db.close()
    logging.info("Database Disconnected")

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(cliente.router, prefix="/v1/cliente", tags=["Cliente"])
app.include_router(usuario.router, prefix="/v1/usuario", tags=["Usuario"])
app.include_router(produto.router, prefix="/v1/produto", tags=["Produto"])

@app.get("/")
def read_root():
    logging.info("root")
    return {"api-version": "0.1.0"}