import logging
from pydantic import BaseModel
from typing import Optional, List
from ...dependencies import get_token_header
from ...database import crud
from fastapi.responses import JSONResponse
from fastapi import (
    APIRouter,
    status,
    Response,
    Header,
    Depends
)

router = APIRouter()
class CreateRoleRequest(BaseModel):
    nome: str

@router.post("/create_role", status_code=status.HTTP_201_CREATED, dependencies=[Depends(get_token_header)])
def create_role(data: CreateRoleRequest):
    try:
        cargo = crud.create_cargo(data.nome)
        return JSONResponse(status_code=status.HTTP_201_CREATED, content={"uuid": str(cargo.idCargo), "Nome": cargo.nome})
    except Exception as e:
        logging.error(e)
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"message": "Erro ao criar o cargo"})