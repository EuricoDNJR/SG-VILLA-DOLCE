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
            "idCliente": "ea68b806-ff49-4604-b52a-89c0db6da721",
            "Pagamento": {
                "valorTotal": 10.00,
                "valorRecebimento": 12.00,
                "valorDevolvido": 2.00,
                "tipoPagamento": "Dinheiro"
            },
            "idCaixa": "852cb8c5-9a79-41a7-8fe2-356f9c2748b0",
            "idProdutos": [
                {
                "idProduto": "d05ecaa4-96d1-4a10-ae81-223ac683affa",
                "quantidade": 2
                },
                {
                "idProduto": "51889c6b-4b30-4fa6-969c-eea8bb786ba0",
                "quantidade": 0.300
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

@router.get("/get_all_orders/", status_code=status.HTTP_200_OK, dependencies=[Depends(get_token_header)])
def get_all_orders():
    """
    Retorna todos os pedidos.
    """
    try:
        logging.info("Getting all orders")
        pedidos = crud.get_all_pedidos()
        if pedidos is None:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"message": "Erro ao buscar pedidos"}
            )
        logging.info("Orders found")
        return JSONResponse(status_code=status.HTTP_200_OK, content=pedidos)
    except Exception as e:
        logging.error(e)
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": "Erro ao buscar pedidos: " + str(e)}
        )

@router.get("/get_order/{idPedido}", status_code=status.HTTP_200_OK, dependencies=[Depends(get_token_header)])
def get_order(idPedido: str):
    """
    Retorna um pedido.
    """
    try:
        logging.info("Getting order")
        pedido = crud.get_pedido_by_id(idPedido=idPedido)
        if pedido is None:
            logging.error("Order not found")
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        logging.info("Order found")
        return JSONResponse(status_code=status.HTTP_200_OK, content=pedido)
    except Exception as e:
        logging.error(e)
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": "Erro ao buscar pedido: " + str(e)}
        )