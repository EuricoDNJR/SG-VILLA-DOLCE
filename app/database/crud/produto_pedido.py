import models
from peewee import DoesNotExist
from decimal import Decimal

def create_produto_pedido(idPedido, idProduto, quantidade, valorVendaUnd, desconto=0.0):
    return models.ProdutoPedido.create(idPedido=idPedido, idProduto=idProduto, quantidade=quantidade, valorVendaUnd=valorVendaUnd, valorTotal = Decimal(str(valorVendaUnd * quantidade)), desconto=Decimal(str(desconto)))

def get_all_produtos_pedidos_by_id(idPedido):
    produtos_pedidos = models.ProdutoPedido.select().where(models.ProdutoPedido.idPedido == idPedido)

    # Verifica se há produtos_pedidos
    if produtos_pedidos.exists():
        # Retorna a lista de produtos_pedidos se houver algum
        return [
            {
                "idProdutoPedido": str(produto_pedido.idProdutoPedido),
                "idProduto": str(produto_pedido.idProduto.idProduto),
                "nome": produto_pedido.idProduto.nome,
                "quantidade": str(produto_pedido.quantidade),
                "desconto": str(produto_pedido.desconto),
                "valorVendaUnd": str(produto_pedido.valorVendaUnd),
                "valorTotal": str(produto_pedido.valorTotal)
            }
            for produto_pedido in produtos_pedidos
        ]
    else:
        # Se não houver produtos_pedidos, retorna None
        return None