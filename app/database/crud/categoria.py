from database import models
from peewee import DoesNotExist


def create_categoria(nome, unidadeMedida):
    return models.Categoria.create(nome=nome, unidadeMedida=unidadeMedida)


def get_categoria_by_id(uuid):
    try:
        categoria = models.Categoria.get(models.Categoria.idCategoria == uuid)

        return categoria
    except DoesNotExist:
        return None


def get_all_categorias():
    # Tenta buscar todos os categorias
    categorias = models.Categoria.select()

    # Verifica se há categorias
    if categorias.exists():
        # Retorna a lista de categorias se houver algum
        return [
            {
                "idCategoria": str(categoria.idCategoria),
                "nome": categoria.nome,
                "unidadeMedida": categoria.unidadeMedida,
            }
            for categoria in categorias
        ]
    else:
        # Se não houver categorias, retorna None
        return None


def update_categoria(uuid, nome=None, unidadeMedida=None):
    try:
        categoria = models.Categoria.get(models.Categoria.idCategoria == uuid)
        if categoria is None:
            return None
        # Atualiza os atributos fornecidos
        if nome is not None:
            categoria.nome = nome
        if unidadeMedida is not None:
            categoria.unidadeMedida = unidadeMedida

        categoria.save()

        return {
            "idCategoria": str(categoria.idCategoria),
            "nome": categoria.nome,
            "unidadeMedida": categoria.unidadeMedida,
        }

    except DoesNotExist:
        return None


def delete_categoria(uuid):
    try:
        categoria = models.Categoria.get(models.Categoria.idCategoria == uuid)
        categoria.delete_instance()
        return True
    except DoesNotExist:
        return None
