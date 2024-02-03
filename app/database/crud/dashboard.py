from datetime import datetime, timedelta
from peewee import fn
from database import models


def categorias_mais_vendidas():
    query = (
        models.Categoria.select(
            models.Categoria.nome,
            fn.SUM(models.ProdutoPedido.quantidade).alias("total_vendido"),
        )
        .join(models.Produto)
        .join(models.ProdutoPedido)
        .join(models.Pedido)
        .where(models.Pedido.data_criacao > datetime.now() - timedelta(days=180))
        .group_by(models.Categoria.nome)
        .order_by(fn.SUM(models.ProdutoPedido.quantidade).desc())
        .limit(5)
    )
    return [
        {"categoria": categoria.nome, "total_vendido": str(categoria.total_vendido)}
        for categoria in query
    ]
