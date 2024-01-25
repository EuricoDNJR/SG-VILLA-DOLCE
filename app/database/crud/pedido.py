from database import models
from peewee import DoesNotExist
from decimal import Decimal

from .produto_pedido import get_all_produtos_pedidos_by_id
from .produto import get_product_by_id


def create_pedido(idCliente, idPagamento, idUsuario, idCaixa, status):
    return models.Pedido.create(
        idCliente=idCliente,
        idPagamento=idPagamento,
        idUsuario=idUsuario,
        idCaixa=idCaixa,
        status=status,
    )


def get_pedido_by_id(idPedido):
    try:
        pedido = models.Pedido.get(models.Pedido.idPedido == idPedido)

        return {
            "idPedido": str(pedido.idPedido),
            "idCliente": str(pedido.idCliente.idCliente),
            "nomeCliente": pedido.idCliente.nome,
            "telefoneCliente": pedido.idCliente.telefone,
            "saldoCliente": str(pedido.idCliente.saldo),
            "idPagamento": str(pedido.idPagamento.idPagamento),
            "valorTotal": str(pedido.idPagamento.valorTotal),
            "valorRecebimento": str(pedido.idPagamento.valorRecebimento),
            "valorDevolvido": str(pedido.idPagamento.valorDevolvido),
            "tipoPagamento": pedido.idPagamento.tipoPagamento,
            "idUsuario": str(pedido.idUsuario.idUsuario),
            "nomeUsuario": pedido.idUsuario.nome,
            "idCaixa": str(pedido.idCaixa.idCaixa),
            "status": pedido.status,
            "idProdutos": get_all_produtos_pedidos_by_id(idPedido),
        }
    except DoesNotExist:
        return None


def get_pedido_object_by_id(idPedido):
    try:
        pedido = models.Pedido.get(models.Pedido.idPedido == idPedido)

        return pedido
    except DoesNotExist:
        return None


def get_all_pedidos():
    # Tenta buscar todos os pedidos
    pedidos = models.Pedido.select()

    # Verifica se há pedidos
    if pedidos.exists():
        # Retorna a lista de pedidos se houver algum
        return [
            {
                "idPedido": str(pedido.idPedido),
                "idCliente": str(pedido.idCliente.idCliente),
                "nomeCliente": pedido.idCliente.nome,
                "telefoneCliente": pedido.idCliente.telefone,
                "idPagamento": str(pedido.idPagamento.idPagamento),
                "valorTotal": str(pedido.idPagamento.valorTotal),
                "valorRecebimento": str(pedido.idPagamento.valorRecebimento),
                "valorDevolvido": str(pedido.idPagamento.valorDevolvido),
                "tipoPagamento": pedido.idPagamento.tipoPagamento,
                "idUsuario": str(pedido.idUsuario.idUsuario),
                "nomeUsuario": pedido.idUsuario.nome,
                "idCaixa": str(pedido.idCaixa.idCaixa),
                "status": pedido.status,
            }
            for pedido in pedidos
        ]
    else:
        # Se não houver pedidos, retorna None
        return None


def get_all_pedidos_pendentes():
    # Tenta buscar todos os pedidos
    pedidos = models.Pedido.select()

    # Verifica se há pedidos
    if pedidos.exists():
        # Retorna a lista de pedidos se houver algum
        return [
            {
                "idPedido": str(pedido.idPedido),
                "idCliente": str(pedido.idCliente.idCliente),
                "nomeCliente": pedido.idCliente.nome,
                "telefoneCliente": pedido.idCliente.telefone,
                "idPagamento": str(pedido.idPagamento.idPagamento),
                "valorTotal": str(pedido.idPagamento.valorTotal),
                "valorRecebimento": str(pedido.idPagamento.valorRecebimento),
                "valorDevolvido": str(pedido.idPagamento.valorDevolvido),
                "tipoPagamento": pedido.idPagamento.tipoPagamento,
                "idUsuario": str(pedido.idUsuario.idUsuario),
                "nomeUsuario": pedido.idUsuario.nome,
                "idCaixa": str(pedido.idCaixa.idCaixa),
                "status": pedido.status,
            }
            for pedido in pedidos
            if pedido.status == "Pendente"
        ]
    else:
        # Se não houver pedidos, retorna None
        return None


def get_all_pedidos_pagos_cancelados():
    # Tenta buscar todos os pedidos
    pedidos = models.Pedido.select()

    # Verifica se há pedidos
    if pedidos.exists():
        # Retorna a lista de pedidos se houver algum
        return [
            {
                "idPedido": str(pedido.idPedido),
                "idCliente": str(pedido.idCliente.idCliente),
                "nomeCliente": pedido.idCliente.nome,
                "telefoneCliente": pedido.idCliente.telefone,
                "idPagamento": str(pedido.idPagamento.idPagamento),
                "valorTotal": str(pedido.idPagamento.valorTotal),
                "valorRecebimento": str(pedido.idPagamento.valorRecebimento),
                "valorDevolvido": str(pedido.idPagamento.valorDevolvido),
                "tipoPagamento": pedido.idPagamento.tipoPagamento,
                "idUsuario": str(pedido.idUsuario.idUsuario),
                "nomeUsuario": pedido.idUsuario.nome,
                "idCaixa": str(pedido.idCaixa.idCaixa),
                "status": pedido.status,
            }
            for pedido in pedidos
            if pedido.status == "Pago" or pedido.status == "Cancelado"
        ]
    else:
        # Se não houver pedidos, retorna None
        return None


def update_balance_client_and_order(pedido):
    produtos_pedidos = models.ProdutoPedido.select().where(
        models.ProdutoPedido.idPedido == pedido.idPedido
    )

    # Verifica se há produtos_pedidos
    if produtos_pedidos.exists():
        # Verifica se nos produtos do pedido há algum com a categoria Açaí para contabilizar no saldo do cliente
        for produto_pedido in produtos_pedidos:
            if (
                produto_pedido.idProduto.categoria.nome == "Açaí"
                and verifier_client_promotion(pedido)
            ):
                if produto_pedido.desconto > Decimal(0.0):
                    pedido.idCliente.saldo -= Decimal(150)
                    if produto_pedido.valorTotal < Decimal(15):
                        pedido.idCliente.saldo += Decimal(15) - produto_pedido.desconto
                    produto_pedido.valorTotal -= produto_pedido.desconto
                    produto_pedido.save()
                    pedido.idCliente.saldo += produto_pedido.valorTotal
                    pedido.idPagamento.valorTotal += produto_pedido.valorTotal
                else:
                    pedido.idCliente.saldo += produto_pedido.valorTotal
                    pedido.idPagamento.valorTotal += produto_pedido.valorTotal
                pedido.idCliente.save()
                pedido.idPagamento.save()
            else:
                # Se for visitante, não contabiliza o saldo do cliente
                pedido.idPagamento.valorTotal += produto_pedido.valorTotal
                pedido.idPagamento.save()
        return True
    else:
        # Se não houver produtos_pedidos, retorna None
        return None


def update_balance_client_and_order_unique(pedido, produto_instance):
    try:
        if (
            produto_instance.idProduto.categoria.nome == "Açaí"
            and verifier_client_promotion(pedido)
        ):
            if produto_instance.desconto > Decimal(0.0):
                pedido.idCliente.saldo -= Decimal(150)
                if produto_instance.valorTotal < Decimal(15):
                    pedido.idCliente.saldo += Decimal(15) - produto_instance.desconto
                produto_instance.valorTotal -= produto_instance.desconto
                produto_instance.save()
                pedido.idCliente.saldo += produto_instance.valorTotal
                pedido.idPagamento.valorTotal += produto_instance.valorTotal
            else:
                pedido.idCliente.saldo += produto_instance.valorTotal
                pedido.idPagamento.valorTotal += produto_instance.valorTotal
            pedido.idCliente.save()
            pedido.idPagamento.save()
        else:
            # Se for visitante, não contabiliza o saldo do cliente
            pedido.idPagamento.valorTotal += produto_instance.valorTotal
            pedido.idPagamento.save()
        return True
    except DoesNotExist:
        # Se ocorrer uma exceção DoesNotExist, retorna None
        return None


def update_balance_client_and_order_cancel(pedido):
    produtos_pedidos = models.ProdutoPedido.select().where(
        models.ProdutoPedido.idPedido == pedido.idPedido
    )

    # Verifica se há produtos_pedidos
    if produtos_pedidos.exists():
        # Verifica se nos produtos do pedido há algum com a categoria Açaí para contabilizar no saldo do cliente
        for produto_pedido in produtos_pedidos:
            if (
                produto_pedido.idProduto.categoria.nome == "Açaí"
                and verifier_client_promotion(pedido)
            ):
                if produto_pedido.desconto > Decimal(0.0):
                    pedido.idCliente.saldo += Decimal(150)
                    produto_pedido.valorTotal += produto_pedido.desconto
                    produto_pedido.save()
                    pedido.idCliente.saldo -= Decimal(15) - produto_pedido.desconto
                    if produto_pedido.valorTotal > Decimal(15):
                        pedido.idCliente.saldo -= produto_pedido.valorTotal - Decimal(
                            15
                        )
                    pedido.idPagamento.valorTotal -= produto_pedido.valorTotal
                    pedido.idPagamento.save()
                else:
                    pedido.idCliente.saldo -= produto_pedido.valorTotal
                    pedido.idPagamento.valorTotal -= produto_pedido.valorTotal
                    pedido.idPagamento.save()
                pedido.idCliente.save()
            else:
                # Se for visitante ou ate mesmo produto normal, so decrementa do valor total do pedido
                pedido.idPagamento.valorTotal -= produto_pedido.valorTotal
                pedido.idPagamento.save()
        return True
    else:
        # Se não houver produtos_pedidos, retorna None
        return None


def update_pedido_status(pedido, status):
    try:
        pedido.status = status
        pedido.save()
        return True
    except DoesNotExist:
        return None


def update_pedido_desconto(pedido, desconto):
    try:
        pedido.desconto = desconto
        pedido.save()
        return True
    except DoesNotExist:
        return None


def delete_replace_quantity_product(idPedido):
    produtos_pedidos = models.ProdutoPedido.select().where(
        models.ProdutoPedido.idPedido == idPedido
    )
    if produtos_pedidos.exists():
        for produto_pedido in produtos_pedidos:
            produto = get_product_by_id(produto_pedido.idProduto.idProduto)
            produto.quantidade += produto_pedido.quantidade
            produto.save()
        return True
    else:
        return None


def delete_produto_pedido(idPedido):
    produtos_pedidos = models.ProdutoPedido.select().where(
        models.ProdutoPedido.idPedido == idPedido
    )
    if produtos_pedidos.exists():
        for produto_pedido in produtos_pedidos:
            produto_pedido.delete_instance()
        return True
    else:
        return None


def delete_pedido(idPedido):
    try:
        pedido = models.Pedido.get(models.Pedido.idPedido == idPedido)
        pedido.delete_instance()
        return True
    except DoesNotExist:
        return None


def verifier_client_promotion(pedido):
    if pedido.idCliente.nome != "Visitante":
        return True
    else:
        return False
