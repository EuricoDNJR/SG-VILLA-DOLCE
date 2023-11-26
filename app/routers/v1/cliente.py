import logging
from typing import Optional
from pydantic import BaseModel
from ...database import crud
from fastapi.responses import JSONResponse
from fastapi import (
    APIRouter,
    HTTPException,
    status,
    Response
)

router = APIRouter()

class ClienteRequest(BaseModel):
    email: Optional[str]
    nome: str
    dataNascimento: Optional[str]
    cpf: Optional[str]
    endereco: Optional[str]
    telefone: str
    saldo: Optional[float]

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

@router.get("/get_client/{telefone}", status_code=status.HTTP_200_OK)
def get_client(telefone: str):
    """
    Retorna um cliente.
    """
    try:
        logging.info("Getting client")
        cliente = crud.get_cliente(telefone=telefone)
        if cliente is None:
            logging.error("Client not found")
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        else:
            logging.info("Client found")
            return JSONResponse(status_code=status.HTTP_200_OK, content=cliente)
    except Exception as e:
        logging.error(e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        )

@router.get("/get_all_clients/", status_code=status.HTTP_200_OK)
def get_all_clients():
    """
    Retorna todos os clientes.
    """
    try:
        logging.info("Getting all clients")
        clientes = crud.get_all_clientes()
        if clientes is not None:
            return JSONResponse(status_code=status.HTTP_200_OK, content=clientes)
        else:
            return Response(status_code=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        logging.error(e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        )