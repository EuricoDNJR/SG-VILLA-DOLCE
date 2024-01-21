import logging
from pydantic import BaseModel
from typing import Optional, List
from dependencies import get_token_header
from database import crud
from fastapi.responses import JSONResponse, Response
from fastapi import (
    APIRouter,
    status,
    Header,
    Depends
)

router = APIRouter()
class CreateRoleRequest(BaseModel):
    nome: str

@router.post("/create_role", status_code=status.HTTP_201_CREATED, dependencies=[Depends(get_token_header)])
def create_role(data: CreateRoleRequest):
    """
    Criação de cargo.
    exemplo de entrada:

        {
            "nome": "Admin"
        }
    """
    try:
        logging.info("Creating role")
        cargo = crud.create_cargo(data.nome)
        logging.info("Role created")
        return JSONResponse(status_code=status.HTTP_201_CREATED, content={"uuid": str(cargo.idCargo), "Nome": cargo.nome})
    except Exception as e:
        logging.error(e)
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"message": "Erro ao criar o cargo"})

@router.get("/get_role/{idCargo}", status_code=status.HTTP_200_OK, dependencies=[Depends(get_token_header)])
def get_role(idCargo: str):
    try:
        logging.info("Getting role")
        cargo = crud.get_cargo_by_id(idCargo)
        if cargo is None:
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message": "Cargo não encontrado"})
        logging.info("Role found")
        return JSONResponse(status_code=status.HTTP_200_OK, content={"uuid": str(cargo.idCargo), "Nome": cargo.nome})
    except Exception as e:
        logging.error(e)
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"message": "Erro ao buscar o cargo"})
    
@router.get("/get_all_roles", status_code=status.HTTP_200_OK, dependencies=[Depends(get_token_header)])
def get_all_roles():
    try:
        logging.info("Getting all roles")
        cargos = crud.get_all_cargos()
        if cargos is None:
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        logging.info("Roles found")
        return JSONResponse(status_code=status.HTTP_200_OK, content=cargos)
    except Exception as e:
        logging.error(e)
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"message": "Erro ao buscar os cargos"})

class UpdateRoleRequest(BaseModel):
    nome: Optional[str] = None    
@router.patch("/update_role/{idCargo}", status_code=status.HTTP_200_OK, dependencies=[Depends(get_token_header)])
def update_role(idCargo: str, data: UpdateRoleRequest):
    try:
        logging.info("Updating role")
        update_cargo = crud.update_cargo(idCargo, data.nome)
        if update_cargo:
            logging.info("Role updated")
            return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Cargo atualizado com sucesso"})
        else:
            logging.info("Role not updated")
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message": "Cargo não existe ou não foi atualizado"})
    except Exception as e:
        logging.error(e)
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"message": "Erro ao atualizar o cargo"})
    
@router.delete("/delete_role/{idCargo}", status_code=status.HTTP_200_OK, dependencies=[Depends(get_token_header)])
def delete_role(idCargo: str):
    try:
        delete_cargo = crud.delete_cargo(idCargo)
        if delete_cargo:
            logging.info("Role deleted")
            return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Cargo deletado com sucesso"})
        else:
            logging.info("Role not deleted")
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message": "Cargo não existe ou não foi deletado"})
    except Exception as e:
        logging.error(e)
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"message": "Erro ao deletar o cargo"})