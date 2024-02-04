from datetime import datetime, timedelta
from peewee import fn
from database import models
from collections import defaultdict
from calendar import month_name


def categorias_mais_vendidas():
    query = (
        models.Categoria.select(
            models.Categoria.nome,
            fn.SUM(models.ProdutoPedido.valorTotal).alias("total_vendido"),
        )
        .join(models.Produto)
        .join(models.ProdutoPedido)
        .join(models.Pedido)
        .where(models.Pedido.data_criacao > datetime.now() - timedelta(days=180))
        .group_by(models.Categoria.nome)
        .order_by(fn.SUM(models.ProdutoPedido.valorTotal).desc())
    )
    return [
        {"categoria": categoria.nome, "total_vendido": str(categoria.total_vendido)}
        for categoria in query
    ]


def clientes_que_mais_compraram():
    query = (
        models.Cliente.select(
            models.Cliente.nome,
            fn.SUM(models.Pagamento.valorTotal).alias("total_comprado"),
        )
        .join(models.Pedido)
        .join(models.Pagamento)
        .where(models.Pedido.data_criacao > datetime.now() - timedelta(days=180))
        .group_by(models.Cliente.nome)
        .order_by(fn.SUM(models.Pagamento.valorTotal).desc())
    )
    return [
        {"cliente": cliente.nome, "total_comprado": str(cliente.total_comprado)}
        for cliente in query
    ]


def produtos_mais_vendidos():
    query = (
        models.Produto.select(
            models.Produto.nome,
            fn.SUM(models.ProdutoPedido.valorTotal).alias("total_vendido"),
        )
        .join(models.ProdutoPedido)
        .join(models.Pedido)
        .where(models.Pedido.data_criacao > datetime.now() - timedelta(days=180))
        .group_by(models.Produto.nome)
        .order_by(fn.SUM(models.ProdutoPedido.valorTotal).desc())
    )
    return [
        {"produto": produto.nome, "total_vendido": str(produto.total_vendido)}
        for produto in query
    ]


from dateutil.relativedelta import relativedelta


def vendas_mensais_do_semestre():
    # Inicializa um dicionário padrão para armazenar os totais de vendas mensais
    vendas_mensais = defaultdict(
        lambda: {"total_vendas": 0, "data_inicio": None, "data_fim": None}
    )

    # Define a data final como a data atual
    data_final = datetime.now()

    # Define a data inicial como seis meses atrás a partir da data atual
    data_inicial = data_final - relativedelta(months=6)

    # Loop para cada mês dentro dos últimos seis meses
    while data_inicial <= data_final:
        # Define a data final do mês atual
        primeiro_dia_mes = data_inicial.replace(day=1)
        ultimo_dia_mes = primeiro_dia_mes + relativedelta(day=31)
        # Executa a consulta para obter o total de vendas para o mês atual
        total_vendas_mes = (
            models.Pagamento.select(fn.SUM(models.Pagamento.valorTotal))
            .join(models.Pedido)
            .where(
                (models.Pedido.data_criacao >= primeiro_dia_mes)
                & (models.Pedido.data_criacao <= ultimo_dia_mes)
            )
            .scalar()
            or 0
        )
        # Armazena o total de vendas para o mês atual no dicionário
        vendas_mensais[primeiro_dia_mes.strftime("%B")] = {
            "total_vendas": str(total_vendas_mes),
            "data_inicio": primeiro_dia_mes.strftime("%d/%m/%Y"),
            "data_fim": ultimo_dia_mes.strftime("%d/%m/%Y"),
        }
        # Atualiza a data inicial para o próximo mês
        data_inicial += relativedelta(months=1)

    return vendas_mensais
