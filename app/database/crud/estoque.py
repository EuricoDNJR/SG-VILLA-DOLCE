import models
from peewee import DoesNotExist
from decimal import Decimal
from produto import get_product_by_id


def create_estoque(idProduto, quantidade, dataEntrada, dataVencimento, observacoes):
    return models.Estoque.create(
        idProduto=idProduto,
        quantidade=quantidade,
        dataEntrada=dataEntrada,
        dataVencimento=dataVencimento,
        observacoes=observacoes,
    )


def get_all_estoques_by_product(uuid):
    estoques = models.Estoque.select().where(models.Estoque.idProduto == uuid)

    # Verifica se há registros de estoque
    if estoques.exists():
        # Retorna a lista de registros de estoque se houver algum
        return [
            {
                "idEstoque": str(estoque.idEstoque),
                "idProduto": str(estoque.idProduto.idProduto),
                "nome": estoque.idProduto.nome,
                "quantidade": str(estoque.quantidade),
                "dataEntrada": str(estoque.dataEntrada),
                "dataVencimento": str(estoque.dataVencimento)
                if estoque.dataVencimento is not None
                else None,
                "observacoes": estoque.observacoes
                if estoque.observacoes is not None
                else None,
            }
            for estoque in estoques
        ]
    else:
        # Se não houver registros de estoque, retorna None
        return None


def get_all_estoques():
    # Tenta buscar todos os registros de estoque
    estoques = models.Estoque.select()

    # Verifica se há registros de estoque
    if estoques.exists():
        # Retorna a lista de registros de estoque se houver algum
        return [
            {
                "idEstoque": str(estoque.idEstoque),
                "idProduto": str(estoque.idProduto.idProduto),
                "nome": estoque.idProduto.nome,
                "quantidade": str(estoque.quantidade),
                "dataEntrada": str(estoque.dataEntrada),
                "dataVencimento": str(estoque.dataVencimento)
                if estoque.dataVencimento is not None
                else None,
                "observacoes": estoque.observacoes
                if estoque.observacoes is not None
                else None,
            }
            for estoque in estoques
        ]
    else:
        # Se não houver registros de estoque, retorna None
        return None


def sum_all_stock_by_product(uuid_product):
    total = Decimal(0.0)
    estoques = models.Estoque.select().where(models.Estoque.idProduto == uuid_product)
    if estoques.exists():
        for estoque in estoques:
            total += estoque.quantidade
        return total
    else:
        return None


def update_stock(
    idEstoque,
    idProduto,
    quantidade=None,
    dataEntrada=None,
    dataVencimento=None,
    observacoes=None,
):
    try:
        estoque = models.Estoque.get(models.Estoque.idEstoque == idEstoque)
        if estoque is None:
            return None
        # Atualiza os atributos fornecidos
        if quantidade is not None:
            try:
                estoque.quantidade = quantidade
                estoque.save()
                quantidade_atualizada = sum_all_stock_by_product(idProduto)
                produto = models.Produto.get(models.Produto.idProduto == idProduto)
                produto.quantidade = Decimal(str(quantidade_atualizada))
                produto.save()
            except Exception as e:
                print(e)
                return None
        if dataEntrada is not None:
            estoque.dataEntrada = dataEntrada
        if dataVencimento is not None:
            estoque.dataVencimento = dataVencimento
        if observacoes is not None:
            estoque.observacoes = observacoes

        estoque.save()

        return {
            "idEstoque": str(estoque.idEstoque),
            "idProduto": str(estoque.idProduto.idProduto),
            "nome": estoque.idProduto.nome,
            "quantidade": str(estoque.quantidade),
            "dataEntrada": str(estoque.dataEntrada),
            "dataVencimento": str(estoque.dataVencimento)
            if estoque.dataVencimento is not None
            else None,
            "observacoes": estoque.observacoes
            if estoque.observacoes is not None
            else None,
        }

    except DoesNotExist:
        return None


def delete_stock_registre(uuid):
    try:
        estoque = models.Estoque.get(models.Estoque.idEstoque == uuid)
        produto = get_product_by_id(estoque.idProduto.idProduto)
        produto.quantidade -= estoque.quantidade
        produto.save()
        estoque.delete_instance()
        return True
    except DoesNotExist:
        return None
