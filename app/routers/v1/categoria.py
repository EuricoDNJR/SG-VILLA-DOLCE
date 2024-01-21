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
class CreateCategoryRequest(BaseModel):
    nome: str
    unidadeMedida: str

@router.post("/create_category", status_code=status.HTTP_201_CREATED, dependencies=[Depends(get_token_header)])
def create_category(data: CreateCategoryRequest):
    """
    Criação de categoria.
    exemplo de entrada:

        {
            "nome": "Açaí",
            "unidadeMedida": "KG"
        }
        
    exemplo de entrada 2:

        {
            "nome": "Refrigerante",
            "unidadeMedida": "UND"
        }
    """
    try:
        logging.info("Creating category")
        categoria = crud.create_categoria(data.nome, data.unidadeMedida)
        logging.info("Category created")
        return JSONResponse(status_code=status.HTTP_201_CREATED, content={"uuid": str(categoria.idCategoria), "Nome": categoria.nome, "Unidade de Medida": categoria.unidadeMedida})
    except Exception as e:
        logging.error(e)
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"message": "Erro ao criar a categoria"})

@router.get("/get_category/{idCategoria}", status_code=status.HTTP_200_OK, dependencies=[Depends(get_token_header)])
def get_category(idCategoria: str):
    try:
        logging.info("Getting category")
        categoria = crud.get_categoria_by_id(idCategoria)
        if categoria is None:
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message": "Categoria não encontrada"})
        logging.info("Category found")
        return JSONResponse(status_code=status.HTTP_200_OK, content={"uuid": str(categoria.idCategoria), "Nome": categoria.nome, "Unidade de Medida": categoria.unidadeMedida})
    except Exception as e:
        logging.error(e)
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"message": "Erro ao buscar a categoria"})
    
@router.get("/get_all_categories", status_code=status.HTTP_200_OK, dependencies=[Depends(get_token_header)])
def get_all_categories():
    try:
        logging.info("Getting all categories")
        categorias = crud.get_all_categorias()
        if categorias is None:
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        logging.info("Categories found")
        return JSONResponse(status_code=status.HTTP_200_OK, content=categorias)
    except Exception as e:
        logging.error(e)
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"message": "Erro ao buscar as categorias"})

class UpdateCategoryRequest(BaseModel):
    nome: Optional[str] = None
    unidadeMedida: Optional[str] = None

@router.patch("/update_category/{idCategoria}", status_code=status.HTTP_200_OK, dependencies=[Depends(get_token_header)])
def update_category(idCategoria: str, data: UpdateCategoryRequest):
    try:
        logging.info("Updating category")
        categoria = crud.update_categoria(idCategoria, data.nome, data.unidadeMedida)
        if categoria is None:
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message": "Categoria não encontrada ou não atualizada"})
        logging.info("Category updated")
        return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Categoria atualizada com sucesso"})
    except Exception as e:
        logging.error(e)
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"message": "Erro ao atualizar a categoria"})

@router.delete("/delete_category/{idCategoria}", status_code=status.HTTP_200_OK, dependencies=[Depends(get_token_header)])
def delete_category(idCategoria: str):
    try:
        logging.info("Deleting category")
        categoria = crud.delete_categoria(idCategoria)
        if categoria is None:
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message": "Categoria não encontrada ou não deletada"})
        logging.info("Category deleted")
        return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Categoria deletada com sucesso"})
    except Exception as e:
        logging.error(e)
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"message": "Erro ao deletar a categoria"})