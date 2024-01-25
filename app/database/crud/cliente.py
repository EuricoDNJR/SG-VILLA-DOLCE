from database import models
from peewee import DoesNotExist
from decimal import Decimal


def create_cliente(email, nome, dataNascimento, cpf, endereco, telefone, saldo):
    return models.Cliente.create(
        email=email,
        nome=nome,
        dataNascimento=dataNascimento,
        cpf=cpf,
        endereco=endereco,
        telefone=telefone,
        saldo=saldo,
    )


def get_cliente(telefone):
    try:
        cliente = models.Cliente.get(models.Cliente.telefone == telefone)

        # Retorna um dicionário contendo apenas atributos não nulos
        return {
            "idCliente": str(cliente.idCliente),
            "email": cliente.email if cliente.email is not None else None,
            "nome": cliente.nome,
            "dataNascimento": str(cliente.dataNascimento)
            if cliente.dataNascimento is not None
            else None,
            "cpf": cliente.cpf if cliente.cpf is not None else None,
            "endereco": cliente.endereco if cliente.endereco is not None else None,
            "telefone": cliente.telefone if cliente.telefone is not None else None,
            "saldo": str(cliente.saldo) if cliente.saldo is not None else None,
        }

    except DoesNotExist:
        return None


def get_client_discounts(uuid):
    try:
        cliente = models.Cliente.get(models.Cliente.idCliente == uuid)
        pontos = cliente.saldo / Decimal(15)
        descontos = pontos * Decimal(0.1)
        valor_prox_desconto = int(descontos + 1) * 150
        return {
            "descontos": str(int(descontos)),
            "pontos": str(int(cliente.saldo / Decimal(15))),
            "saldo": str(cliente.saldo),
            "proximo_desconto": str(valor_prox_desconto - cliente.saldo),
        }
    except DoesNotExist:
        return None


def get_all_clientes():
    # Tenta buscar todos os clientes
    clientes = models.Cliente.select()

    # Verifica se há clientes
    if clientes.exists():
        # Retorna a lista de clientes se houver algum
        return [
            {
                "idCliente": str(cliente.idCliente),
                "email": cliente.email if cliente.email is not None else None,
                "nome": cliente.nome,
                "dataNascimento": str(cliente.dataNascimento)
                if cliente.dataNascimento is not None
                else None,
                "cpf": cliente.cpf if cliente.cpf is not None else None,
                "endereco": cliente.endereco if cliente.endereco is not None else None,
                "telefone": cliente.telefone if cliente.telefone is not None else None,
                "saldo": str(cliente.saldo) if cliente.saldo is not None else None,
            }
            for cliente in clientes
        ]
    else:
        # Se não houver clientes, retorna None
        return None


def update_cliente(
    uuid,
    telefone=None,
    email=None,
    nome=None,
    dataNascimento=None,
    cpf=None,
    endereco=None,
    saldo=None,
):
    try:
        cliente = models.Cliente.get(models.Cliente.idCliente == uuid)
        if cliente.nome == "Visitante":
            return False
        if cliente is None:
            return None
        # Atualiza os atributos fornecidos
        if telefone is not None:
            cliente.telefone = telefone
        if email is not None:
            cliente.email = email
        if nome is not None:
            cliente.nome = nome
        if dataNascimento is not None:
            cliente.dataNascimento = dataNascimento
        if cpf is not None:
            cliente.cpf = cpf
        if endereco is not None:
            cliente.endereco = endereco
        if saldo is not None:
            cliente.saldo = saldo

        cliente.save()

        return {
            "idCliente": str(cliente.idCliente),
            "email": cliente.email if cliente.email is not None else None,
            "nome": cliente.nome,
            "dataNascimento": str(cliente.dataNascimento)
            if cliente.dataNascimento is not None
            else None,
            "cpf": cliente.cpf if cliente.cpf is not None else None,
            "endereco": cliente.endereco if cliente.endereco is not None else None,
            "telefone": cliente.telefone if cliente.telefone is not None else None,
            "saldo": str(cliente.saldo) if cliente.saldo is not None else None,
        }

    except DoesNotExist:
        return None


def delete_cliente(uuid):
    try:
        cliente = models.Cliente.get(models.Cliente.idCliente == uuid)
        cliente.delete_instance()
        return True
    except DoesNotExist:
        return None
