from database import models
from peewee import DoesNotExist
from collections import defaultdict

def open_caixa(
    saldoInicial,
    dataAbertura,
    observacoes,
    horaAbertura,
    idUsuarioAbertura,
):
    return models.Caixa.create(
        saldoInicial=saldoInicial,
        dataAbertura=dataAbertura,
        horaAbertura=horaAbertura,
        observacoes=observacoes,
        idUsuarioAbertura=idUsuarioAbertura,
        idUsuarioFechamento=idUsuarioAbertura,
    )


def close_caixa(uuid, dataFechamento, idUsuarioFechamento):
    try:
        caixa = models.Caixa.get(models.Caixa.idCaixa == uuid)

        if caixa is None:
            return None
        if caixa.aberto == True:
            caixa.dataFechamento = dataFechamento
            caixa.aberto = False
            caixa.idUsuarioFechamento = idUsuarioFechamento
        caixa.save()

        return True

    except DoesNotExist:
        return False


def get_caixa(date):
    caixa = models.Caixa.get(models.Caixa.dataAbertura == date)

    if caixa.aberto == False:
        return caixa
    else:
        None

def get_caixa_by_id(uuid):
    try:
        caixa = models.Caixa.get(models.Caixa.idCaixa == uuid)
        return {
            "idCaixa": str(caixa.idCaixa),
            "saldoInicial": str(caixa.saldoInicial),
            "dataAbertura": str(caixa.dataAbertura),
            "dataFechamento": str(caixa.dataFechamento),
            "aberto": caixa.aberto,
            "observacoes": caixa.observacoes,
            "somenteDinheiro": str(caixa.somenteDinheiro),
            "SaldoFinal": str(caixa.saldoFinal),
            "nomeUsuarioAbertura": caixa.idUsuarioAbertura.nome,
            "nomeUsuarioFechamento": str(caixa.idUsuarioFechamento.nome),
        }
    except DoesNotExist:
        return None

def get_all_caixa():
    # Tenta buscar todos os caixas
    caixas = models.Caixa.select()

    # Verifica se há usuários
    if caixas.exists():
        # Retorna a lista de usuários se houver algum
        return [
            {
                "idCaixa": str(caixa.idCaixa),
                "saldoInicial": str(caixa.saldoInicial),
                "dataAbertura": str(caixa.dataAbertura),
                "dataFechamento": str(caixa.dataFechamento),
                "aberto": caixa.aberto,
                "observacoes": caixa.observacoes,
                "somenteDinheiro": str(caixa.somenteDinheiro),
                "saldoFinal": str(caixa.saldoFinal),
                "nomeUsuarioAbertura": caixa.idUsuarioAbertura.nome,
                "nomeUsuarioFechamento": str(caixa.idUsuarioFechamento.nome),
            }
            for caixa in caixas  # if caixa.aberto == False
        ]
    else:
        # Se não houver usuários, retorna None
        return None


def get_first_caixa_open():
    try:
        caixa = models.Caixa.select().where(models.Caixa.aberto == True).get()
        return {
            "idCaixa": str(caixa.idCaixa),
            "saldoInicial": str(caixa.saldoInicial),
            "dataAbertura": str(caixa.dataAbertura),
            "dataFechamento": str(caixa.dataFechamento),
            "aberto": caixa.aberto,
            "observacoes": caixa.observacoes,
            "somenteDinheiro": str(caixa.somenteDinheiro),
            "saldoFinal": str(caixa.saldoFinal),
        }
    except DoesNotExist:
        return None


def update_novo_saldoInicial(uuid, novoSaldo=None):
    try:
        caixa = models.Caixa.get(models.Caixa.idCaixa == uuid)

        if caixa is None:
            return None
        if novoSaldo is not None:
            caixa.saldoInicial = novoSaldo
        caixa.save()

        return {"saldoInicial": caixa.saldoInicial}

    except DoesNotExist:
        return None


def update_balance_caixa_pedido(idCaixa, valorTotal, tipoPagamento):
    try:
        caixa = models.Caixa.get(models.Caixa.idCaixa == idCaixa)
        caixa.saldoFinal += valorTotal
        caixa.save()
        if tipoPagamento == "Dinheiro":
            caixa.somenteDinheiro += valorTotal
            caixa.save()
        return True
    except DoesNotExist:
        return None


def get_all_paid_and_canceled_orders_caixa(idCaixa):
    pedidos = models.Pedido.select().where(models.Pedido.idCaixa == idCaixa)

    # Verifica se há pedidos
    if pedidos.exists():
        # Retorna a lista de pedidos pagos ou pendentes se houver algum
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


def get_all_pendent_orders_caixa(idCaixa):
    pedidos = models.Pedido.select().where(models.Pedido.idCaixa == idCaixa)

    # Retorna a lista de pedidos pagos ou pendentes se houver algum
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

def get_sum_type_payment_by_id(idCaixa):
    try:
        # Inicializa um dicionário padrão para armazenar o somatório das vendas por tipo de pagamento
        somatorio_pagamentos = defaultdict(int)

        # Executa a consulta para obter os pedidos associados ao caixa especificado
        pedidos_caixa = models.Pedido.select().where(models.Pedido.idCaixa == idCaixa)

        # Calcula o somatório das vendas por tipo de pagamento
        for pedido in pedidos_caixa:
            pagamento = pedido.idPagamento
            tipo_pagamento = pagamento.tipoPagamento
            somatorio_pagamentos[tipo_pagamento] += pagamento.valorTotal
        
        for tipo_payment in somatorio_pagamentos:
            somatorio_pagamentos[tipo_payment] = str(somatorio_pagamentos[tipo_payment])

        return somatorio_pagamentos
    
    except Exception:
        return None

def get_inputs_outputs_by_id(idCaixa):
    try:
        somatorio_entradas_saidas = {"entradas": 0, "saidas": 0}

        pagamentos_caixa = models.Pagamento.select().join(models.Pedido).where(models.Pedido.idCaixa == idCaixa)

        # Calcula o somatório das entradas e saídas
        for pagamento in pagamentos_caixa:
            somatorio_entradas_saidas["entradas"] += pagamento.valorRecebimento
            somatorio_entradas_saidas["saidas"] += pagamento.valorDevolvido

        for tipo in somatorio_entradas_saidas:
            somatorio_entradas_saidas[tipo] = str(somatorio_entradas_saidas[tipo])
        
        return somatorio_entradas_saidas
    
    except Exception:
        return None

def get_quant_orders_stats_by_id(idCaixa):
    try:

        somatorio_pedidos_status = {"nao_cancelados": 0, "cancelados": 0}

        pedidos_caixa = models.Pedido.select().where(models.Pedido.idCaixa == idCaixa)

        for pedido in pedidos_caixa:
            if pedido.status in ["Pago", "Pendente"]:
                somatorio_pedidos_status["nao_cancelados"] += 1
            elif pedido.status == "Cancelado":
                somatorio_pedidos_status["cancelados"] += 1

        return somatorio_pedidos_status
    
    except Exception:
        return None

def average_products_per_order_by_id(idCaixa):
    try:
        total_produtos = 0
        total_pedidos = 0

        pedidos_caixa = models.Pedido.select().where(models.Pedido.idCaixa == idCaixa)

        for pedido in pedidos_caixa:
            total_produtos += pedido.quantidade_produtos_pedido
            total_pedidos += 1

        media_produtos_por_pedido = total_produtos / total_pedidos if total_pedidos > 0 else 0

        return media_produtos_por_pedido
    
    except Exception:
        return None