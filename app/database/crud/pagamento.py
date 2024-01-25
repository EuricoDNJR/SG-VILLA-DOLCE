import models
from peewee import DoesNotExist
from decimal import Decimal

def create_pagamento(valorRecebimento=0.0, valorDevolvido=0.0, tipoPagamento=None):
    return models.Pagamento.create(valorTotal=Decimal(0.0), valorRecebimento=Decimal(str(valorRecebimento)), valorDevolvido=Decimal(str(valorDevolvido)), tipoPagamento=tipoPagamento)

def update_pagamento(pedido, tipoPagamento, valorRecebimento=0.0, valorDevolvido=0.0):
    try:
        pedido.idPagamento.valorRecebimento = Decimal(str(valorRecebimento))
        pedido.idPagamento.valorDevolvido = Decimal(str(valorDevolvido))
        pedido.idPagamento.tipoPagamento = tipoPagamento
        pedido.idPagamento.save()
        return True
    except DoesNotExist:
        return None

def update_pagamento_valorTotal(idPagamento, valorTotalProduto):
    try:
        idPagamento.valorTotal += valorTotalProduto
        idPagamento.save()
        return True
    except DoesNotExist:
        return None

def delete_pagamento(idPagamento):
    try:
        pagamento = models.Pagamento.get(models.Pagamento.idPagamento == idPagamento)
        pagamento.delete_instance()
        return True
    except DoesNotExist:
        return None
