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

class PagamentoPedido(BaseModel):
    valorTotal: float
    valorRecebimento: float
    valorDevolvido: float
    tipoPagamento: str

class ProdutoPedido(BaseModel):
    idProduto: str 
    quantidade: float

class CreateOrderRequest(BaseModel):
    idCliente: str
    Pagamento: PagamentoPedido
    idCaixa: str
    idProdutos: List[ProdutoPedido]

@router.post("/create_order/", status_code=status.HTTP_201_CREATED, dependencies=[Depends(get_token_header)])
def create_order(data: CreateOrderRequest, jwt_token: str = Header()):
    """
    Criação de pedido.
    exemplo de entrada:

        {
            "idCliente": "6ffe7706-4c87-4f3b-8ecb-b8c44b1c416b",
            "Pagamento": {
                "valorTotal": 10.00,
                "valorRecebimento": 12.00,
                "valorDevolvido": 2.00,
                "tipoPagamento": "Dinheiro"
            },
            "idCaixa": "6bacd806-aeaa-4bc4-b1e3-a670596816c6",
            "idProdutos": [
                {
                "idProduto": "d7bb1db7-6f65-4d7d-a1e0-270e9a306603",
                "quantidade": 2
                }
            ]
        }
    """
    
    logging.info("Getting user")
    logging.info("Creating order by user: " + jwt_token)
    logging.info("Creating instance of payment")
    pagamento = crud.create_pagamento(
        valorTotal=data.Pagamento.valorTotal, 
        valorRecebimento=data.Pagamento.valorRecebimento, 
        valorDevolvido=data.Pagamento.valorDevolvido, 
        tipoPagamento=data.Pagamento.tipoPagamento)
    if pagamento is None:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": "Erro ao criar pagamento"}
        )
    logging.info("Payment created")
    logging.info("Creating instance of order")
    pedido = crud.create_pedido(
        idCliente=data.idCliente,
        idPagamento=pagamento.idPagamento,
        idUsuario=jwt_token,
        idCaixa=data.idCaixa,
    )
    if pedido is None:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": "Erro ao criar pedido"}
        )
    logging.info("Order created")
    try:
        logging.info("adding products to order")
        for produto in data.idProdutos:
            crud.create_produto_pedido(
                idPedido=pedido.idPedido,
                idProduto=produto.idProduto,
                quantidade=produto.quantidade
            )
        logging.info("Products added to order")
    except Exception as e:
        logging.error(e)
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": "Erro ao adicionar produtos ao pedido"}
        )
    try:
        logging.info("Updating quantity of products")
        for produto in data.idProdutos:
            if crud.update_quantity_product(produto.idProduto, produto.quantidade):
                logging.info("Quantity of product {} updated".format(produto.idProduto))
            else:
                logging.info("Quantity of product {} not updated".format(produto.idProduto))
        logging.info("Quantity of products updated")
    except Exception as e:
        logging.error(e)
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": "Erro ao atualizar quantidade de produtos"}
        )
    try:
        logging.info("Updating balance of client")
        if crud.update_balance_client(data.idCliente, data.Pagamento.valorTotal):
            logging.info("Balance of client updated")
        else:
            logging.info("Balance of client not updated")
    except Exception as e:
        logging.error(e)
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": "Erro ao atualizar saldo do cliente"}
        )
    logging.info("Order created successfully")
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={"uuid": str(pedido.idPedido), "message": "Pedido criado com sucesso"})


