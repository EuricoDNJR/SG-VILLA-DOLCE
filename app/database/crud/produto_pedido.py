from decimal import Decimal

from database import models


def create_produto_pedido(idPedido, idProduto, quantidade, valorVendaUnd, desconto=0.0):
    return models.ProdutoPedido.create(
        idPedido=idPedido,
        idProduto=idProduto,
        quantidade=quantidade,
        valorVendaUnd=valorVendaUnd,
        valorTotal=Decimal(str(valorVendaUnd * quantidade)),
        desconto=Decimal(str(desconto)),
    )


def get_all_produtos_pedidos_by_id(idPedido):
    produtos_pedidos = models.ProdutoPedido.select().where(
        models.ProdutoPedido.idPedido == idPedido
    )

    if not produtos_pedidos.exists():
        return None

    # Consolidate by product + unit value so the order reopens without duplicate lines.
    grouped = {}
    ordered_keys = []
    for produto_pedido in produtos_pedidos:
        key = (
            str(produto_pedido.idProduto.idProduto),
            Decimal(str(produto_pedido.valorVendaUnd)),
        )
        if key not in grouped:
            grouped[key] = {
                "idProdutoPedido": str(produto_pedido.idProdutoPedido),
                "idProduto": str(produto_pedido.idProduto.idProduto),
                "nome": produto_pedido.idProduto.nome,
                "quantidade": Decimal("0"),
                "desconto": Decimal("0"),
                "valorVendaUnd": Decimal(str(produto_pedido.valorVendaUnd)),
                "valorTotal": Decimal("0"),
            }
            ordered_keys.append(key)

        grouped[key]["quantidade"] += Decimal(str(produto_pedido.quantidade))
        grouped[key]["desconto"] += Decimal(str(produto_pedido.desconto))
        grouped[key]["valorTotal"] += Decimal(str(produto_pedido.valorTotal))

    return [
        {
            "idProdutoPedido": grouped[key]["idProdutoPedido"],
            "idProduto": grouped[key]["idProduto"],
            "nome": grouped[key]["nome"],
            "quantidade": str(grouped[key]["quantidade"]),
            "desconto": str(grouped[key]["desconto"]),
            "valorVendaUnd": str(grouped[key]["valorVendaUnd"]),
            "valorTotal": str(grouped[key]["valorTotal"]),
        }
        for key in ordered_keys
    ]
