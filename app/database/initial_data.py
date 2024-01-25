import os
import dotenv
import models
from crud.cargo import create_cargo
from crud.tipo_pagamento import create_tipo_pagamento
from crud.cliente import create_cliente
from crud.usuario import create_usuario

from passlib.hash import bcrypt
from peewee import DoesNotExist
from decimal import Decimal


def create_initial_values():
    dotenv.load_dotenv()

    # Verifica se os cargos já existem
    try:
        models.Cargo.get(models.Cargo.nome == "Admin")
    except DoesNotExist:
        create_cargo("Admin")

    try:
        models.Cargo.get(models.Cargo.nome == "Colaborador")
    except DoesNotExist:
        create_cargo("Colaborador")

    # Verifica se os tipos de pagamento já existem
    try:
        models.TipoPagamento.get(models.TipoPagamento.nome == "Dinheiro")
    except DoesNotExist:
        create_tipo_pagamento("Dinheiro")

    try:
        models.TipoPagamento.get(models.TipoPagamento.nome == "Pix")
    except DoesNotExist:
        create_tipo_pagamento("Pix")

    try:
        models.TipoPagamento.get(models.TipoPagamento.nome == "Cartão de Crédito")
    except DoesNotExist:
        create_tipo_pagamento("Cartão de Crédito")

    try:
        models.TipoPagamento.get(models.TipoPagamento.nome == "Cartão de Débito")
    except DoesNotExist:
        create_tipo_pagamento("Cartão de Débito")

    # Verifica se o cliente 'Visitante' já existe
    try:
        models.Cliente.get(models.Cliente.telefone == "00000000000")
    except DoesNotExist:
        create_cliente(
            email="",
            nome="Visitante",
            dataNascimento="1000-01-01",
            cpf="00000000000",
            endereco="",
            telefone="00000000000",
            saldo=Decimal(0.0),
        )

    # Verifica se ao menos um usuário com cargo de 'Admin' já existe
    try:
        models.Usuario.get(models.Usuario.cargo == "Admin")
    except DoesNotExist:
        create_usuario(
            email="adminpadrao@gmail.com",
            senha=bcrypt.using(rounds=12).hash(os.getenv("ADMIN_PASSWORD")),
            nome="Admin",
            dataNascimento="1000-01-01",
            cpf="00000000000",
            endereco="Rua Admin",
            telefone="0",
            cargo="Admin",
        )
