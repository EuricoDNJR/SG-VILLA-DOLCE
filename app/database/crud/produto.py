import models
from peewee import DoesNotExist
from decimal import Decimal

def create_produto(nome, descricao, categoria, valorVenda):
    return models.Produto.create(nome=nome, descricao=descricao, categoria=categoria, valorVenda=valorVenda)

def get_product_by_id(uuid):
    try:
        produto = models.Produto.get(models.Produto.idProduto == uuid)
        return produto
    except DoesNotExist:
        return None

def get_all_produtos():
    # Tenta buscar todos os produtos
    produtos = models.Produto.select()

    # Verifica se há produtos
    if produtos.exists():
        # Retorna a lista de produtos se houver algum
        return [
            {
                "idProduto": str(produto.idProduto),
                "nome": produto.nome,
                "descricao": produto.descricao if produto.descricao is not None else None,
                "categoria": produto.categoria.nome,
                "valorVenda": str(produto.valorVenda),
                "unidadeMedida": produto.categoria.unidadeMedida,
                "quantidade": str(produto.quantidade)
            }
            for produto in produtos
        ]
    else:
        # Se não houver produtos, retorna None
        return None
    
def update_product(uuid, nome=None, descricao=None, categoria=None, valorCusto=None, valorVenda=None, unidadeMedida=None):
    try:
        produto = models.Produto.get(models.Produto.idProduto == uuid)
        if produto is None:
            return None
        # Atualiza os atributos fornecidos
        if nome is not None:
            produto.nome = nome
        if descricao is not None:
            produto.descricao = descricao
        if categoria is not None:
            produto.categoria.nome = categoria
            produto.categoria.save()
        if valorVenda is not None:
            produto.valorVenda = valorVenda
        if unidadeMedida is not None:
            produto.categoria.unidadeMedida = unidadeMedida
            produto.categoria.save()

        produto.save()

        return {
            "idProduto": str(produto.idProduto),
            "nome": produto.nome,
            "descricao": produto.descricao if produto.descricao is not None else None,
            "categoria": produto.categoria.nome,
            "valorVenda": str(produto.valorVenda),
            "unidadeMedida": produto.categoria.unidadeMedida,
            "quantidade": str(produto.quantidade)
        }

    except DoesNotExist:
        return None

def update_quantity_product(uuid, quantidade):
    try:
        produto = models.Produto.get(models.Produto.idProduto == uuid)
        produto.quantidade -= Decimal(str(quantidade))
        produto.save()
        return True
    except DoesNotExist:
        return None
    
def update_stock_product(uuid, quantidade):
    try:
        produto = models.Produto.get(models.Produto.idProduto == uuid)
        produto.quantidade += Decimal(str(quantidade))
        produto.save()
        return True
    except DoesNotExist:
        return None
    
def delete_product(uuid):
    try:

        models.Estoque.delete().where(models.Estoque.idProduto == uuid).execute()

        produto = models.Produto.get(models.Produto.idProduto == uuid)
        produto.delete_instance()
        return True
    except DoesNotExist:
        return None