import models
from peewee import DoesNotExist
from decimal import Decimal
from passlib.hash import bcrypt

def create_usuario(email, senha, nome, dataNascimento, cpf, endereco, telefone, cargo):
    return models.Usuario.create(email=email, senha=senha, nome=nome, dataNascimento=dataNascimento, cpf=cpf, endereco=endereco, telefone=telefone, cargo=cargo)

def get_usuario(telefone):
    try:
        return models.Usuario.get(models.Usuario.telefone == telefone)
    except DoesNotExist:
        return None

def get_usuario_by_id(uuid):
    try:
        usuario = models.Usuario.get(models.Usuario.idUsuario == uuid)

        return {
            "idUsuario": str(usuario.idUsuario),
            "email": usuario.email,
            "nome": usuario.nome,
            "dataNascimento": str(usuario.dataNascimento),
            "cpf": usuario.cpf,
            "endereco": usuario.endereco,
            "telefone": usuario.telefone,
            "cargo": usuario.cargo
        }
    except DoesNotExist:
        return None

def get_all_users():
    # Tenta buscar todos os usuários
    usuarios = models.Usuario.select()

    # Verifica se há usuários
    if usuarios.exists():
        # Retorna a lista de usuários se houver algum
        return [
            {
                "idUsuario": str(usuario.idUsuario),
                "email": usuario.email,
                "nome": usuario.nome,
                "dataNascimento": str(usuario.dataNascimento),
                "cpf": usuario.cpf,
                "endereco": usuario.endereco,
                "telefone": usuario.telefone,
                "cargo": usuario.cargo
            }
            for usuario in usuarios
        ]
    else:
        # Se não houver usuários, retorna None
        return None

def update_user(uuid, telefone=None, email=None, senha=None, nome=None, dataNascimento=None, cpf=None, endereco=None, cargo=None):
    try:
        usuario = models.Usuario.get(models.Usuario.idUsuario == uuid)
        if usuario is None:
            return None
        # Atualiza os atributos fornecidos
        if telefone is not None:
            usuario.telefone = telefone
        if email is not None:
            usuario.email = email
        if senha is not None:
            hashed_password = bcrypt.using(rounds=12).hash(senha)
            usuario.senha = hashed_password
        if nome is not None:
            usuario.nome = nome
        if dataNascimento is not None:
            usuario.dataNascimento = dataNascimento
        if cpf is not None:
            usuario.cpf = cpf
        if endereco is not None:
            usuario.endereco = endereco
        if cargo is not None:
            usuario.cargo = cargo

        usuario.save()

        return {
            "idUsuario": str(usuario.idUsuario),
            "email": usuario.email,
            "nome": usuario.nome,
            "dataNascimento": str(usuario.dataNascimento),
            "cpf": usuario.cpf,
            "endereco": usuario.endereco,
            "telefone": usuario.telefone,
            "cargo": usuario.cargo
        }

    except DoesNotExist:
        return None

def delete_user(uuid):
    try:
        usuario = models.Usuario.get(models.Usuario.idUsuario == uuid)
        usuario.delete_instance()
        return True
    except DoesNotExist:
        return None