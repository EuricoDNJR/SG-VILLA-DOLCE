import json
import logging

from ...database import crud
from fastapi import (
    APIRouter,
    Form,
    HTTPException,
    status,
)

router = APIRouter()

@router.post("/create_client/", status_code=status.HTTP_201_CREATED)
def create_client(data: str = Form()):
    try:
        logging.info("Receiving data")
        json_data = json.loads(data)
        logging.info("Data received")
        logging.info("Creating client")
        cliente = crud.create_cliente(
            json_data["email"],
            json_data["nome"],
            json_data["dataNascimento"],
            json_data["cpf"],
            json_data["endereco"],
            json_data["telefone"],
            json_data["saldo"],
        )
        logging.info("Client created")
        return {"uuid": str(cliente.idCliente), "Nome": cliente.nome}
    except Exception as e:
        logging.error(e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        )