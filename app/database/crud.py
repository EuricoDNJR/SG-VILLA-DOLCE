from . import models
from peewee import DoesNotExist

def create_cliente(email, nome, dataNascimento, cpf, endereco, telefone, saldo):
    return models.Cliente.create(email=email, nome=nome, dataNascimento=dataNascimento, cpf=cpf, endereco=endereco, telefone=telefone, saldo=saldo)

def create_usuario(email, senha, nome, dataNascimento, cpf, endereco, telefone, cargo):
    return models.Usuario.create(email=email, senha=senha, nome=nome, dataNascimento=dataNascimento, cpf=cpf, endereco=endereco, telefone=telefone, cargo=cargo)

def get_usuario(telefone):
    try:
        return models.Usuario.get(models.Usuario.telefone == telefone)
    except DoesNotExist:
        return None

def get_all_users():
    try:
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
                    "dataNascimento": usuario.dataNascimento.isoformat(),
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
    except DoesNotExist:
        # Se ocorrer uma exceção DoesNotExist, retorna None
        return None