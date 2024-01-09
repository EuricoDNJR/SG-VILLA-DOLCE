import logging
import json
from typing import Optional
from pydantic import BaseModel
from ...database import crud
from ...dependencies import get_token_header
from fastapi.responses import JSONResponse
from fastapi import (
    APIRouter,
    status,
    Response,
    Header,
    Depends
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

@router.post("/create_client/", status_code=status.HTTP_201_CREATED, dependencies=[Depends(get_token_header)])
def create_client(data: ClienteRequest, jwt_token: str = Header()):
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
        logging.info("Creating client by user: " + jwt_token)
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
        return JSONResponse(status_code=status.HTTP_201_CREATED, content={"uuid": str(cliente.idCliente), "Nome": cliente.nome})
        
    except Exception as e:
        logging.error(e)
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": "Erro ao criar cliente: " + str(e)})

@router.get("/get_client/{telefone}", status_code=status.HTTP_200_OK, dependencies=[Depends(get_token_header)])
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
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": "Erro ao buscar cliente: " + str(e)})

@router.get("/get_all_clients/", status_code=status.HTTP_200_OK, dependencies=[Depends(get_token_header)])
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
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": "Erro ao buscar clientes: " + str(e)})

class ClienteUpdateRequest(BaseModel):
    telefone: Optional[str] = None
    email: Optional[str] = None
    nome: Optional[str] = None
    dataNascimento: Optional[str] = None
    cpf: Optional[str] = None
    endereco: Optional[str] = None
    saldo: Optional[float] = None
    
@router.patch("/update_cliente/{idCliente}", status_code=status.HTTP_200_OK, dependencies=[Depends(get_token_header)])
def update_cliente(
    data: ClienteUpdateRequest,
    idCliente: str
):
    '''
    Atualiza um cliente.
    exemplo de entrada:
    
        {
            "telefone": "999999999",
            "email": "flavinhodopneu@gmail.com",
            "nome": "Flavio",
            "dataNascimento": "1990/10/08",
            "cpf": "13578924680",
            "endereco": "Rua bem ali na UFPI",
            "saldo": 0
        }
    '''
    try:
        logging.info("Updating client")
        update_cliente = crud.update_cliente(
            uuid=idCliente,
            telefone=data.telefone,
            email=data.email,
            nome=data.nome,
            dataNascimento=data.dataNascimento,
            cpf=data.cpf,
            endereco=data.endereco,
            saldo=data.saldo
        )
        if update_cliente:
            logging.info("Client updated")
            return JSONResponse(status_code=status.HTTP_200_OK, content=update_cliente)
        else:
            logging.error("Client not found")
            return Response(status_code=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        logging.error(e)
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": "Erro ao atualizar cliente: " + str(e)})
    
@router.delete("/delete_cliente/{idCliente}", status_code=status.HTTP_200_OK, dependencies=[Depends(get_token_header)])
def delete_cliente(idCliente: str):
    try:
        logging.info("Deleting client")
        delete_cliente = crud.delete_cliente(uuid=idCliente)
        if delete_cliente:
            logging.info("Client deleted")
            return JSONResponse(status_code=status.HTTP_200_OK, content={'message': 'Cliente deletado com sucesso'})
        else:
            logging.error("Client not found")
            return Response(status_code=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        logging.error(e)
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": "Erro ao deletar cliente: " + str(e)})
    
@router.get("/get_client_discounts/{idCliente}", status_code=status.HTTP_200_OK, dependencies=[Depends(get_token_header)])
def get_client_discounts(idCliente: str):
    try:
        logging.info("Getting client discounts")
        discounts = crud.get_client_discounts(uuid=idCliente)
        if discounts is not None:
            logging.info("Discounts found")
            return JSONResponse(status_code=status.HTTP_200_OK, content=discounts)
        else:
            logging.error("Discounts not found")
            return Response(status_code=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        logging.error(e)
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": "Erro ao buscar descontos do cliente: " + str(e)})