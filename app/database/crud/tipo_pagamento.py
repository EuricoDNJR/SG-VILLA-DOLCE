from database import models
from peewee import DoesNotExist
from collections import defaultdict
from datetime import datetime

def create_tipo_pagamento(nome):
    return models.TipoPagamento.create(nome=nome)


def get_tipo_pagamento_by_id(uuid):
    try:
        tipo_pagamento = models.TipoPagamento.get(
            models.TipoPagamento.idTipoPagamento == uuid
        )

        return tipo_pagamento
    except DoesNotExist:
        return None


def get_all_tipo_pagamentos():
    tipo_pagamentos = models.TipoPagamento.select()

    # Verifica se há tipo_pagamentos
    if tipo_pagamentos.exists():
        # Retorna a lista de tipo_pagamentos se houver algum
        return [
            {
                "idTipoPagamento": str(tipo_pagamento.idTipoPagamento),
                "nome": tipo_pagamento.nome,
            }
            for tipo_pagamento in tipo_pagamentos
        ]
    else:
        # Se não houver tipo_pagamentos, retorna None
        return None


def update_tipo_pagamento(uuid, nome=None):
    try:
        tipo_pagamento = models.TipoPagamento.get(
            models.TipoPagamento.idTipoPagamento == uuid
        )
        if tipo_pagamento is None:
            return None
        # Atualiza os atributos fornecidos
        if nome is not None:
            tipo_pagamento.nome = nome

        tipo_pagamento.save()

        return {
            "idTipoPagamento": str(tipo_pagamento.idTipoPagamento),
            "nome": tipo_pagamento.nome,
        }

    except DoesNotExist:
        return None


def delete_payment_type(uuid):
    try:
        tipo_pagamento = models.TipoPagamento.get(
            models.TipoPagamento.idTipoPagamento == uuid
        )
        tipo_pagamento.delete_instance()
        return True
    except DoesNotExist:
        return None

def somatorio_vendas_tipos_pagamento_mes_atual():
    # Inicializa um dicionário padrão para armazenar o somatório das vendas por tipo de pagamento
    somatorio_pagamentos = defaultdict(int)

    # Define a data final como a data atual
    data_final = datetime.now()

    # Define a data inicial como o primeiro dia do mês atual
    primeiro_dia_mes = datetime(data_final.year, data_final.month, 1)

    # Executa a consulta para obter os pedidos do mês atual
    pedidos_do_mes = models.Pedido.select().where(
        (models.Pedido.data_criacao >= primeiro_dia_mes)
        & (models.Pedido.data_criacao <= data_final)
    )

    # Calcula o somatório das vendas por tipo de pagamento
    for pedido in pedidos_do_mes:
        pagamento = pedido.idPagamento
        tipo_pagamento = pagamento.tipoPagamento
        somatorio_pagamentos[tipo_pagamento] += pagamento.valorTotal

    for tipo_pagamento, valor in somatorio_pagamentos.items():
        somatorio_pagamentos[tipo_pagamento] = str(valor)
    
    return somatorio_pagamentos