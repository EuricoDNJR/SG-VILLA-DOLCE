import models
from peewee import DoesNotExist

def create_cargo(nome):
    return models.Cargo.create(nome=nome)

def get_all_cargos():
    # Tenta buscar todos os cargos
    cargos = models.Cargo.select()

    # Verifica se há cargos
    if cargos.exists():
        # Retorna a lista de cargos se houver algum
        return [
            {
                "idCargo": str(cargo.idCargo),
                "nome": cargo.nome
            }
            for cargo in cargos
        ]
    else:
        # Se não houver cargos, retorna None
        return None

def get_cargo_by_id(uuid):
    try:
        cargo = models.Cargo.get(models.Cargo.idCargo == uuid)

        return cargo
    except DoesNotExist:
        return None

def update_cargo(uuid, nome=None):
    try:
        cargo = models.Cargo.get(models.Cargo.idCargo == uuid)
        if cargo is None:
            return None
        # Atualiza os atributos fornecidos
        if nome is not None:
            cargo.nome = nome

        cargo.save()

        return {
            "idCargo": str(cargo.idCargo),
            "nome": cargo.nome
        }

    except DoesNotExist:
        return None

def delete_cargo(uuid):
    try:
        cargo = models.Cargo.get(models.Cargo.idCargo == uuid)
        cargo.delete_instance()
        return True
    except DoesNotExist:
        return None