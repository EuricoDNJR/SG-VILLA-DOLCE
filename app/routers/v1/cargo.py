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

@router.get("/get_role/{idCargo}", status_code=status.HTTP_200_OK, dependencies=[Depends(get_token_header)])
def get_role(idCargo: str):
    try:
        cargo = crud.get_cargo_by_id(idCargo)
        return JSONResponse(status_code=status.HTTP_200_OK, content={"uuid": str(cargo.idCargo), "Nome": cargo.nome})
    except Exception as e:
        logging.error(e)
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"message": "Erro ao buscar o cargo"})
    
@router.get("/get_all_roles", status_code=status.HTTP_200_OK, dependencies=[Depends(get_token_header)])
def get_all_roles():
    try:
        cargos = crud.get_all_cargos()
        if cargos is None:
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        return JSONResponse(status_code=status.HTTP_200_OK, content=cargos)
    except Exception as e:
        logging.error(e)
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"message": "Erro ao buscar os cargos"})

class UpdateRoleRequest(BaseModel):
    nome: Optional[str] = None    
@router.patch("/update_role/{idCargo}", status_code=status.HTTP_200_OK, dependencies=[Depends(get_token_header)])
def update_role(idCargo: str, data: UpdateRoleRequest):
    try:
        update_cargo = crud.update_cargo(idCargo, data.nome)
        if update_cargo:
            return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Cargo atualizado com sucesso"})
        else:
            return Response(status_code=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        logging.error(e)
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"message": "Erro ao atualizar o cargo"})
    
@router.delete("/delete_role/{idCargo}", status_code=status.HTTP_200_OK, dependencies=[Depends(get_token_header)])
def delete_role(idCargo: str):
    try:
        delete_cargo = crud.delete_cargo(idCargo)
        if delete_cargo:
            return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Cargo deletado com sucesso"})
        else:
            return Response(status_code=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        logging.error(e)
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"message": "Erro ao deletar o cargo"})