import models
from peewee import DoesNotExist


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
