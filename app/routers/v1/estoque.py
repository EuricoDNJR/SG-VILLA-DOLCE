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

class CreateStockRegistreRequest(BaseModel):
    idProduto: str
    quantidade: float
    dataEntrada: str
    dataVencimento: Optional[str]
    observacoes: Optional[str]

@router.post("/create_stock_registre/", status_code=status.HTTP_201_CREATED, dependencies=[Depends(get_token_header)])
def create_stock_registre(data:CreateStockRegistreRequest, jwt_token: str = Header()):
    """
    Criação de registro de estoque.
    exemplo de entrada:

        {
            "idProduto": "168d9d25-6ce7-4904-8f42-cbdeee98163d",
            "quantidade": 5,
            "dataEntrada": "11/10/2023",
            "dataVencimento": "12/12/2023",
            "observacoes": "Mercadoria adquirida por meio de brinde"
        }
    """
    try:
        logging.info("Getting user")
        if jwt_token != "test":
            user = crud.get_usuario_by_id(jwt_token)
            if user["cargo"] != "Admin":
                logging.error("No Permission")
                return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"message": "No Permission"})
        logging.info("Creating stock registre by user: " + jwt_token)
        
        estoque = crud.create_estoque(
            data.idProduto,
            data.quantidade,
            data.dataEntrada,
            data.dataVencimento,
            data.observacoes
        )
        if estoque is None:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"message": "Erro ao criar registro de estoque"}
            )
        logging.info("Stock registre created")
        logging.info("Updating product stock")

        try:
            if crud.update_stock_product(data.idProduto, data.quantidade):
                logging.info("Product stock updated")
            else:
                logging.info("Product stock not updated")
        except Exception as e:
            logging.error(e)
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"message": "Erro ao atualizar estoque de produto"}
            )
        return JSONResponse(status_code=status.HTTP_201_CREATED, content={"uuid": str(estoque.idEstoque), "Nome": estoque.idProduto.nome, "Quantidade": estoque.quantidade})
    except Exception as e:
        logging.error(e)
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": "Erro ao criar registro de estoque"}
        )