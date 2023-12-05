import logging
from pydantic import BaseModel
from typing import Optional
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

class CreateProductRequest(BaseModel):
    nome: str
    descricao: Optional[str]
    categoria: str
    valorCusto: float
    valorVenda: float
    unidadeMedida: str

@router.post("/create_product/", status_code=status.HTTP_201_CREATED, dependencies=[Depends(get_token_header)])
def create_product(data:CreateProductRequest, jwt_token: str = Header()):
    """
    Criação de produto.
    exemplo de entrada:

        {
            "nome": "Refrigerante Fys",
            "descricao": "latinha 300ml",
            "categoria": "Refrigerante",
            "valorCusto": 40.50,
            "valorVenda": 4.99,
            "unidadeMedida": "UND"
        }
    """
    try:
        
        logging.info("Getting user")
        if jwt_token != "test":
            user = crud.get_usuario_by_id(jwt_token)
            if user["cargo"] != "Admin":
                logging.error("No Permission")
                return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"message": "No Permission"})
            
        logging.info("Creating product by user: " + jwt_token)
        produto = crud.create_produto(
            data.nome,
            data.descricao,
            data.categoria,
            data.valorCusto,
            data.valorVenda,
            data.unidadeMedida
        )
        if produto is None:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"message": "Erro ao criar produto"}
            )
        logging.info("Product created")
        return JSONResponse(status_code=status.HTTP_201_CREATED, content={"uuid": str(produto.idProduto), "Nome": produto.nome})
    except Exception as e:
        logging.error(e)
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": "Erro ao criar produto: " + str(e)}
        )

@router.get("/get_all_products/", status_code=status.HTTP_200_OK, dependencies=[Depends(get_token_header)])
def get_all_products():
    """
    Retorna todos os produtos.
    """
    try:
        logging.info("Getting user")
        logging.info("Getting all products")
        produtos = crud.get_all_produtos()
        if produtos is None:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"message": "Erro ao buscar produtos"}
            )
        logging.info("Products found")
        return JSONResponse(status_code=status.HTTP_200_OK, content=produtos)
    except Exception as e:
        logging.error(e)
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": "Erro ao buscar produtos: " + str(e)}
        )

@router.get("/get_product/{uuid}", status_code=status.HTTP_200_OK, dependencies=[Depends(get_token_header)])
def get_product(uuid: str):
    """
    Retorna um produto.
    """
    try:
        logging.info("Getting product")
        produto = crud.get_product_by_id(uuid=uuid)
        if produto is None:
            logging.error("Product not found")
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        logging.info("Product found")
        return JSONResponse(status_code=status.HTTP_200_OK, content={
            "uuid": str(produto.idProduto), 
            "Nome": produto.nome, 
            "Descrição": produto.descricao if produto.descricao is not None else None, 
            "Categoria": produto.categoria, 
            "Valor de Custo": str(produto.valorCusto), 
            "Valor de Venda": str(produto.valorVenda), 
            "Unidade de Medida": produto.unidadeMedida})
    except Exception as e:
        logging.error(e)
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": "Erro ao buscar produto: " + str(e)}
        )