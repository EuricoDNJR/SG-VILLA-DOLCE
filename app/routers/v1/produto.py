import logging
from pydantic import BaseModel
from typing import Optional
from dependencies import get_token_header
from database import crud
from fastapi.responses import JSONResponse
from fastapi import (
    APIRouter,
    status,
    Header,
    Depends
)

router = APIRouter()

class CreateProductRequest(BaseModel):
    nome: str
    descricao: Optional[str]
    categoria: str
    valorVenda: float

@router.post("/create_product/", status_code=status.HTTP_201_CREATED, dependencies=[Depends(get_token_header)])
def create_product(data:CreateProductRequest, jwt_token: str = Header()):
    """
    Criação de produto.
    exemplo de entrada:

        {
            "nome": "Refrigerante Fys",
            "descricao": "latinha 300ml",
            "categoria": "59a4b512-a866-49d5-8103-3bebc632b892",
            "valorVenda": 4.99
        }
        
    exemplo de entrada 2:

        {
            "nome": "AÇAÍ BÚFALO (3,3Kg)",
            "descricao": "AÇAÍ BÚFALO (3,3Kg). 9366.",
            "categoria": "c209b2e1-54b3-4b46-9ddb-3359436ee1af",
            "valorVenda": 40.00
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
            data.valorVenda
        )
        if produto is None:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"message": "Erro ao criar produto"}
            )
        logging.info("Product created")
        categoria = crud.get_categoria_by_id(produto.categoria)
        return JSONResponse(status_code=status.HTTP_201_CREATED, content={"uuid": str(produto.idProduto), "Nome": produto.nome, "categoria": categoria.nome, "unidadeMedida": categoria.unidadeMedida, "valorVenda": str(produto.valorVenda), "idCategoria": str(categoria.idCategoria), "quantidade": str(produto.quantidade)})
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
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message": "Produto não encontrado"})
        logging.info("Product found")
        return JSONResponse(status_code=status.HTTP_200_OK, content={
            "uuid": str(produto.idProduto), 
            "Nome": produto.nome, 
            "Descrição": produto.descricao if produto.descricao is not None else None, 
            "Categoria": produto.categoria.nome,
            "Valor de Venda": str(produto.valorVenda), 
            "Unidade de Medida": produto.categoria.unidadeMedida,
            "Quantidade em Estoque": str(produto.quantidade)})
    except Exception as e:
        logging.error(e)
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": "Erro ao buscar produto: " + str(e)}
        )

class UpdateProductRequest(BaseModel):
    nome: Optional[str]
    descricao: Optional[str]
    categoria: Optional[str]
    valorVenda: Optional[float]
    unidadeMedida: Optional[str]
   
@router.patch("/update_product/", status_code=status.HTTP_200_OK, dependencies=[Depends(get_token_header)])
def update_product(data: UpdateProductRequest, uuid: str, jwt_token: str = Header()):
    """
    Atualização de produto.
    exemplo de entrada:

        {
            "nome": "Acai",
            "descricao": "Acai da Amazonia",
            "categoria": "Sorvete",
            "valorVenda": 30.00,
            "unidadeMedida": "KG"
        }
    """
    try:
        logging.info("Verifying permission")
        if jwt_token != "test":
            user = crud.get_usuario_by_id(jwt_token)
            if user["cargo"] != "Admin":
                logging.error("No Permission")
                return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"message": "No Permission"})
        logging.info("Updating product")
        produto = crud.update_product(
            uuid=uuid,
            nome=data.nome,
            descricao=data.descricao,
            categoria=data.categoria,
            valorVenda=data.valorVenda,
            unidadeMedida=data.unidadeMedida
        )
        if produto is None:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"message": "Erro ao atualizar produto"}
            )
        logging.info("Product updated")
        return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Produto atualizado com sucesso"})
    except Exception as e:
        logging.error(e)
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": "Erro ao atualizar produto: " + str(e)}
        )

@router.delete("/delete_product/{uuid}", status_code=status.HTTP_200_OK, dependencies=[Depends(get_token_header)])
def delete_product(uuid: str, jwt_token: str = Header()):
    """
    Deleção de produto.
    """
    try:
        logging.info("Verifying permission")
        if jwt_token != "test":
            user = crud.get_usuario_by_id(jwt_token)
            if user["cargo"] != "Admin":
                logging.error("No Permission")
                return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"message": "No Permission"})
        logging.info("Deleting product")
        produto = crud.delete_product(uuid)
        if produto is None:
            logging.error("Product not found")
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message": "Produto não encontrado"})
        logging.info("Product deleted")
        return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Produto deletado com sucesso"})
    except Exception as e:
        logging.error(e)
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": "Erro ao deletar produto: " + str(e)}
        )