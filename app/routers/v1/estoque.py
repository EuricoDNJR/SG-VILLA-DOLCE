import logging
from pydantic import BaseModel
from typing import Optional
from dependencies import get_token_header
from database.crud.usuario import get_usuario_by_id
from database.crud.estoque import (
    create_estoque,
    get_all_estoques,
    get_all_estoques_by_product,
    update_stock,
    delete_stock_registre,
)
from database.crud.produto import update_stock_product
from fastapi.responses import JSONResponse, Response
from fastapi import APIRouter, status, Header, Depends

router = APIRouter()


class CreateStockRegistreRequest(BaseModel):
    idProduto: str
    quantidade: float
    dataEntrada: str
    dataVencimento: Optional[str] = None
    observacoes: Optional[str] = None


@router.post(
    "/create_stock_registre/",
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(get_token_header)],
)
def create_stock_registre(data: CreateStockRegistreRequest, jwt_token: str = Header()):
    """
    Criação de registro de estoque.
    exemplo de entrada:

        {
            "idProduto": "168d9d25-6ce7-4904-8f42-cbdeee98163d",
            "quantidade": 5,
            "dataEntrada": "2023-10-01",
            "dataVencimento": "2024-06-01",
            "observacoes": "Mercadoria adquirida por meio de brinde"
        }
    """
    try:
        logging.info("Getting user")
        if jwt_token != "test":
            user = get_usuario_by_id(jwt_token)
            if user["cargo"] != "Admin":
                logging.error("No Permission")
                return JSONResponse(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    content={"message": "No Permission"},
                )
        logging.info("Creating stock registre by user: " + jwt_token)

        estoque = create_estoque(
            data.idProduto,
            data.quantidade,
            data.dataEntrada,
            data.dataVencimento,
            data.observacoes,
        )
        if estoque is None:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"message": "Erro ao criar registro de estoque"},
            )
        logging.info("Stock registre created")
        logging.info("Updating product stock")

        try:
            if update_stock_product(data.idProduto, data.quantidade):
                logging.info("Product stock updated")
            else:
                logging.info("Product stock not updated")
        except Exception as e:
            logging.error(e)
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"message": "Erro ao atualizar estoque de produto"},
            )
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={
                "uuid": str(estoque.idEstoque),
                "Nome": estoque.idProduto.nome,
                "Quantidade": estoque.quantidade,
            },
        )
    except Exception as e:
        logging.error(e)
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": "Erro ao criar registro de estoque"},
        )


@router.get(
    "/get_all_stock_registres/",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(get_token_header)],
)
def get_all_stock_registres():
    """
    Retorna todos os registros de estoque.
    """
    try:
        logging.info("Getting all stock registres")
        estoques = get_all_estoques()
        if estoques is None:
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        logging.info("Stock registres found")
        return JSONResponse(status_code=status.HTTP_200_OK, content=estoques)
    except Exception as e:
        logging.error(e)
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": "Erro ao buscar registros de estoque"},
        )


@router.get(
    "/get_all_stock_registre/{idProduto}",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(get_token_header)],
)
def get_all_stock_registres_by_id(idProduto: str):
    """
    Retorna todos os registros de estoque de um produto.
    """
    try:
        logging.info("Getting all stock registres")
        estoques = get_all_estoques_by_product(idProduto)
        if estoques is None:
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        logging.info("Stock registres found")
        return JSONResponse(status_code=status.HTTP_200_OK, content=estoques)
    except Exception as e:
        logging.error(e)
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": "Erro ao buscar registros de estoque"},
        )


class UpdateStockRegistreRequest(BaseModel):
    idProduto: str
    quantidade: Optional[float] = None
    dataEntrada: Optional[str] = None
    dataVencimento: Optional[str] = None
    observacoes: Optional[str] = None


@router.patch(
    "/update_stock_registre/{idEstoque}",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(get_token_header)],
)
def update_stock_registre(
    data: UpdateStockRegistreRequest, idEstoque: str, jwt_token: str = Header()
):
    """
    Atualização de registro de estoque.
    exemplo de entrada:

        {
            "idProduto": "168d9d25-6ce7-4904-8f42-cbdeee98163d",
            "quantidade": 5,
            "dataEntrada": "2023/10/14",
            "dataVencimento": "2023/11/20",
            "observacoes": "Mercadoria adquirida por meio de brinde"
        }
    """
    try:
        logging.info("Getting user")
        if jwt_token != "test":
            user = get_usuario_by_id(jwt_token)
            if user["cargo"] != "Admin":
                logging.error("No Permission")
                return JSONResponse(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    content={"message": "No Permission"},
                )
        logging.info("Updating stock registre by user: " + jwt_token)
        estoque = update_stock(
            idEstoque=idEstoque,
            idProduto=data.idProduto,
            quantidade=data.quantidade,
            dataEntrada=data.dataEntrada,
            dataVencimento=data.dataVencimento,
            observacoes=data.observacoes,
        )
        if estoque is None:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"message": "Erro ao atualizar registro de estoque"},
            )
        logging.info("Stock registre updated")
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"message": "Registro de estoque atualizado com sucesso"},
        )
    except Exception as e:
        logging.error(e)
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": "Erro ao atualizar registro de estoque"},
        )


@router.delete(
    "/delete_stock_registre/{idEstoque}",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(get_token_header)],
)
def delete_stock_registre_by_id(idEstoque: str, jwt_token: str = Header()):
    """
    Exclusao de registro de estoque.
    """
    try:
        logging.info("Getting user")
        if jwt_token != "test":
            user = get_usuario_by_id(jwt_token)
            if user["cargo"] != "Admin":
                logging.error("No Permission")
                return JSONResponse(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    content={"message": "No Permission"},
                )
        logging.info("Deleting stock registre by user: " + jwt_token)
        estoque = delete_stock_registre(idEstoque)
        if estoque is None:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "message": "Erro ao deletar registro de estoque - Registro de estoque não encontrado"
                },
            )
        logging.info("Stock registre deleted")
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"message": "Registro de estoque deletado com sucesso"},
        )
    except Exception as e:
        logging.error(e)
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": "Erro ao deletar registro de estoque"},
        )
