import logging
from pydantic import BaseModel
from typing import Optional, List
from decimal import Decimal
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
    valorRecebimento: Optional[float] = 0.0
    valorDevolvido: Optional[float] = 0.0
    tipoPagamento: Optional[str] = None

class ProdutoPedido(BaseModel):
    idProduto: str 
    quantidade: float
    valorVendaUnd: float
    desconto: Optional[float] = 0.0

class CreateOrderRequest(BaseModel):
    idCliente: str
    Pagamento: PagamentoPedido
    idCaixa: str
    idProdutos: List[ProdutoPedido]
    status: str
    desconto: bool

@router.post("/create_order/", status_code=status.HTTP_201_CREATED, dependencies=[Depends(get_token_header)])
def create_order(data: CreateOrderRequest, jwt_token: str = Header()):
    """
    Criação de pedido.
    exemplo de entrada:

        {
            "idCliente": "ba3412d7-fa4b-4f44-a1d7-d3f50ce11956",
            "Pagamento": {
                "valorTotal": 10.00,
                "valorRecebimento": 30.00,
                "valorDevolvido": 20.00,
                "tipoPagamento": "Dinheiro"
            },
            "idCaixa": "037543ea-5449-451f-88dd-3370af50f7aa",
            "idProdutos": [
                {
                "idProduto": "4718af40-ee5d-486f-8a8a-d1ffe3604a2a",
                "quantidade": 0.450,
                "valorVendaUnd": 40.00,
                "desconto": 15.00
                },
                {
                "idProduto": "8c9228f3-8d77-47fd-89e3-1ee7bb9b376e",
                "quantidade": 2,
                "valorVendaUnd": 5.00
                }
            ],
            "status": "Pago",
            "desconto": true
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
        status=data.status,
        desconto=data.desconto
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
                quantidade=produto.quantidade,
                valorVendaUnd=produto.valorVendaUnd,
                desconto=produto.desconto
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
    if data.status == "Pago":
        try:
            logging.info("Updating caixa balance")
            if crud.update_balance_caixa_pedido(data.idCaixa, data.Pagamento.valorTotal, data.Pagamento.tipoPagamento):
                logging.info("Balance of caixa updated")
            else:
                logging.info("Balance of caixa not updated")
        except Exception as e:
            logging.error(e)
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"message": "Erro ao atualizar saldo do caixa"}
            )
        try:
            logging.info("Updating balance of client")
            if crud.update_balance_client(pedido):
                logging.info("Balance of client updated")
            else:
                logging.info("Balance of client not updated")
        except Exception as e:
            logging.error(e)
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"message": str(e)}
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
            return Response(status_code=status.HTTP_204_NO_CONTENT)
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

class AddInOrderRequest(BaseModel):
    idProdutos: List[ProdutoPedido]
    valorTotal: float
    desconto: bool
    
@router.patch("/add_in_order/{idPedido}", status_code=status.HTTP_200_OK, dependencies=[Depends(get_token_header)])
def add_in_order(idPedido: str, data: AddInOrderRequest):
    """
    Adiciona produtos em um pedido.
    exemplo de entrada:

        {
            "idProdutos": [
                {
                "idProduto": "d05ecaa4-96d1-4a10-ae81-223ac683affa",
                "quantidade": 2
                },
                {
                "idProduto": "51889c6b-4b30-4fa6-969c-eea8bb786ba0",
                "quantidade": 0.300,
                "desconto": 15.00
                }
            ],
            valorTotal: 15.00,
            desconto: True
        }
    """
    logging.info("Getting order by id")
    try:
        pedido = crud.get_pedido_object_by_id(idPedido=idPedido)
        if pedido is None:
            logging.error("Order not found")
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        logging.info("Order found")
    except Exception as e:
        logging.error(e)
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": "Erro ao buscar pedido: " + str(e)}
        )
    try:
        logging.info("Verifying if order is pending")
        if pedido.status != "Pendente":
            logging.info("Order not pending")
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"message": "Pedido não pendente, por favor, para adicionar produtos ao pedido o mesmo deve estar em estado pendente!!"}
            )
        logging.info("Order stats verified")
    except Exception as e:
        logging.error(e)
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message":"Erro ao verificar status do pedido: " + str(e)}
        )
    try:
        for produto in data.idProdutos:
            crud.create_produto_pedido(
                idPedido=pedido.idPedido,
                idProduto=produto.idProduto,
                quantidade=produto.quantidade,
                desconto=produto.desconto
            )
            if crud.update_quantity_product(produto.idProduto, produto.quantidade):
                logging.info("Quantity of product {} updated".format(produto.idProduto))
            else:
                logging.info("Quantity of product {} not updated".format(produto.idProduto))
        logging.info("Updating total value of order")
        if crud.update_pagamento_valorTotal(pedido.idPagamento, data.valorTotal):
            logging.info("Total value of order updated")
        else:
            logging.info("Total value of order not updated")
        logging.info("Updating discount of order")
        if crud.update_pedido_desconto(pedido, data.desconto):
            logging.info("Discount of order updated")
        else:
            logging.info("Discount of order not updated")
        logging.info("New product(s) added to order")
        return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Produto(s) adicionado(s) ao pedido com sucesso"})
    except Exception as e:
        logging.error(e)
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": str(e)}
        )

class FinishOrderRequest(BaseModel):
    valorRecebimento: float
    valorDevolvido: Optional[float] = 0.0
    tipoPagamento: str

@router.patch("/finish_order/{idPedido}", status_code=status.HTTP_200_OK, dependencies=[Depends(get_token_header)])
def finish_order(idPedido: str, data: FinishOrderRequest):
    """
    Finaliza um pedido.
    exemplo de entrada:
    
        {
            "valorRecebimento": 50.00,
            "valorDevolvido": 29.20,
            "tipoPagamento": "Dinheiro"
        }
    """
    logging.info("Getting order by id")
    try:
        pedido = crud.get_pedido_object_by_id(idPedido=idPedido)
        if pedido is None:
            logging.error("Order not found")
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        logging.info("Order found")
    except Exception as e:
        logging.error(e)
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": "Erro ao buscar pedido: " + str(e)}
        )
    try:
        logging.info("Verifying if order is already finished")
        if pedido.status == "Pago":
            logging.info("Order already finished")
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"message": "Pedido já finalizado"}
            )
        logging.info("Order not finished")
    except Exception as e:
        logging.error(e)
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message":"Erro ao verificar status do pedido: " + str(e)}
        )
    try:
        logging.info("Updating payment of order")
        if crud.update_pagamento(idPagamento=pedido.idPagamento, valorRecebimento=data.valorRecebimento, valorDevolvido=data.valorDevolvido, tipoPagamento=data.tipoPagamento):
            logging.info("Payment of order updated")
        else:
            logging.info("Payment of order not updated")
    except Exception as e:
        logging.error(e)
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": str(e)}
        )
    try:
        logging.info("Updating caixa balance")
        if crud.update_balance_caixa_pedido(pedido.idCaixa, pedido.idPagamento.valorTotal, pedido.idPagamento.tipoPagamento):
            logging.info("Balance of caixa updated")
        else:
            logging.info("Balance of caixa not updated")
    except Exception as e:
        logging.error(e)
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": str(e)}
        )
    try:
        logging.info("Updating balance of client")
        if crud.update_balance_client(pedido):
            logging.info("Balance of client updated")
        else:
            logging.info("Balance of client not updated")
    except Exception as e:
        logging.error(e)
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": str(e)}
        )
    try:
        logging.info("Updating status of order")
        if crud.update_pedido_status(pedido, "Pago"):
            logging.info("Status of order updated")
        else:
            logging.info("Status of order not updated")
    except Exception as e:
        logging.error(e)
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": str(e)}
        )
    logging.info("Order finished successfully")
    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Pedido finalizado com sucesso", "saldo_cliente": str(pedido.idCliente.saldo)})

@router.patch("/cancel_order/{idPedido}", status_code=status.HTTP_200_OK, dependencies=[Depends(get_token_header)])
def cancel_order(idPedido: str):
    """
    Cancela um pedido.
    """
    logging.info("Getting order by id")
    try:
        pedido = crud.get_pedido_object_by_id(idPedido=idPedido)
        if pedido is None:
            logging.error("Order not found")
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        logging.info("Order found")
    except Exception as e:
        logging.error(e)
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": "Erro ao buscar pedido: " + str(e)}
        )
    try:
        logging.info("Verifying if order is already canceled")
        if pedido.status == "Cancelado":
            logging.info("Order already canceled")
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"message": "Pedido já cancelado"}
            )
        logging.info("Order not canceled")
    except Exception as e:
        logging.error(e)
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message":"Erro ao verificar status do pedido: " + str(e)}
        )
    try:
        logging.info("Updating payment of order")
        if crud.update_pagamento(idPagamento=pedido.idPagamento, valorRecebimento=0.0, valorDevolvido=0.0, tipoPagamento="Cancelado"):
            logging.info("Payment of order updated")
        else:
            logging.info("Payment of order not updated")
    except Exception as e:
        logging.error(e)
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": str(e)}
        )
    if pedido.status == "Pago":
        try:
            logging.info("Updating caixa balance")
            if crud.update_balance_caixa_pedido(pedido.idCaixa, -abs(pedido.idPagamento.valorTotal), pedido.idPagamento.tipoPagamento):
                logging.info("Balance of caixa updated")
            else:
                logging.info("Balance of caixa not updated")
        except Exception as e:
            logging.error(e)
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"message": str(e)}
            )
        try:
            logging.info("Updating balance of client")
            if crud.update_balance_client_cancel(pedido):
                logging.info("Balance of client updated")
            else:
                logging.info("Balance of client not updated")
        except Exception as e:
            logging.error(e)
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"message": str(e)}
            )
    try: 
        logging.info("getting products of order and replacing quantity")
        if crud.delete_replace_quantity_product(pedido.idPedido):
            logging.info("Quantity of products replaced")
        else:
            logging.info("Quantity of products not replaced")
    except Exception as e:
        logging.error(e)
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message":"Erro ao recolocar produtos do pedido: " + str(e)}
        )
    try:
        logging.info("Updating status of order")
        if crud.update_pedido_status(pedido, "Cancelado"):
            logging.info("Status of order updated")
        else:
            logging.info("Status of order not updated")
    except Exception as e:
        logging.error(e)
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": str(e)}
        )
    logging.info("Order canceled successfully")
    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Pedido cancelado com sucesso"})
    
@router.delete("/delete_order/{idPedido}", status_code=status.HTTP_200_OK, dependencies=[Depends(get_token_header)])
def delete_order(idPedido: str, jwt_token: str = Header()):
    """
    Deleta um pedido.
    """
    logging.info("Deleting order")
    logging.info("Deleting products of order {} by {}".format(idPedido, jwt_token))
    logging.info("Getting order")
    try:
        pedido = crud.get_pedido_by_id(idPedido=idPedido)
        if pedido is None:
            logging.error("Order not found")
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        logging.info("Order found")
    except Exception as e:
        logging.error(e)
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": "Erro ao buscar pedido: " + str(e)}
        )
    try:
        logging.info("Verifying if order is not canceled")
        if pedido["status"] != "Cancelado":
            logging.info("Order not canceled")
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"message": "Pedido não cancelado, por favor, cancele o pedido antes de excluí-lo!!"}
            )
        logging.info("Order canceled")
    except Exception as e:
        logging.error(e)
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message":"Erro ao verificar status do pedido: " + str(e)}
        )
    try:
        logging.info("Deleting products of order")
        if crud.delete_produto_pedido(pedido["idPedido"]):
            logging.info("Products of order deleted")
        else:
            logging.info("Products of order not deleted")
    except Exception as e:
        logging.error(e)
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": "Erro ao deletar produtos do pedido: " + str(e)}
        )
    try:
        logging.info("Deleting order")
        if crud.delete_pedido(pedido["idPedido"]):
            logging.info("Order deleted")
        else:
            logging.info("Order not deleted")
    except Exception as e:
        logging.error(e)
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": "Erro deletar pedido: " + str(e)}
        )
    try:
        logging.info("Deleting payment of order")
        if crud.delete_pagamento(pedido["idPagamento"]):
            logging.info("Payment of order deleted")
        else:
            logging.info("Payment of order not deleted")
    except Exception as e:
        logging.error(e)
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": "Erro ao deletar pagamento do pedido: " + str(e)}
        )
    logging.info("Order deleted successfully")
    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Pedido deletado com sucesso"})