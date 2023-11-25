import json
import logging
from pydantic import BaseModel
from ...database import crud
from fastapi import (
    APIRouter,
    HTTPException,
    status,
)

router = APIRouter()

class ClienteRequest(BaseModel):
    email: str
    nome: str
    dataNascimento: str
    cpf: str
    endereco: str
    telefone: str
    saldo: float

@router.post("/create_client/", status_code=status.HTTP_201_CREATED)
def create_client(data: ClienteRequest):
    """
    Criação de usuário.
    exemplo de entrada:
    
        {
            "email": "test3@gmail.com",
            "nome": "Nome do Usuário",
            "dataNascimento": "1990-01-01",
            "cpf": "12345678301",
            "endereco": "Rua Exemplo, 123",
            "telefone": "123456789",
            "saldo": "100.00"
        }
    """
    try:
        logging.info("Creating client")
        cliente = crud.create_cliente(
            data.email,
            data.nome,
            data.dataNascimento,
            data.cpf,
            data.endereco,
            data.telefone,
            data.saldo,
        )
        logging.info("Client created")
        return {"uuid": str(cliente.idCliente), "Nome": cliente.nome}
    except Exception as e:
        logging.error(e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        )