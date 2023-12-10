from . import models
from peewee import DoesNotExist
from passlib.hash import bcrypt
from decimal import Decimal


def create_cliente(email, nome, dataNascimento, cpf, endereco, telefone, saldo):
    return models.Cliente.create(email=email, nome=nome, dataNascimento=dataNascimento, cpf=cpf, endereco=endereco, telefone=telefone, saldo=saldo)

def create_usuario(email, senha, nome, dataNascimento, cpf, endereco, telefone, cargo):
    return models.Usuario.create(email=email, senha=senha, nome=nome, dataNascimento=dataNascimento, cpf=cpf, endereco=endereco, telefone=telefone, cargo=cargo)

def create_produto(nome, descricao, categoria, valorCusto, valorVenda, unidadeMedida):
    return models.Produto.create(nome=nome, descricao=descricao, categoria=categoria, valorCusto=valorCusto, valorVenda=valorVenda, unidadeMedida=unidadeMedida)

def create_estoque(idProduto, quantidade, dataEntrada, dataVencimento, observacoes):
    return models.Estoque.create(idProduto=idProduto, quantidade=quantidade, dataEntrada=dataEntrada, dataVencimento=dataVencimento, observacoes=observacoes)

def open_caixa(saldoInicial, dataAbertura, observacoes, horaAbertura):
    return models.Caixa.create(saldoInicial=saldoInicial, dataAbertura=dataAbertura,horaAbertura = horaAbertura, observacoes=observacoes, somenteDinheiro = saldoInicial)

def close_caixa(uuid, dataFechamento):
    try:

        caixa = models.Caixa.get(models.Caixa.idCaixa == uuid)

        if caixa is None:
            return None
        if caixa.aberto == True:
            caixa.dataFechamento = dataFechamento
            caixa.aberto = False
        caixa.save()

        return True
    
    except DoesNotExist:
        return False
    
def get_caixa(date):

    try:

        caixa = models.Caixa.get(models.Caixa.dataAbertura == date)

        if caixa.aberto == False:
            return caixa
        else:
            None 
    except:
        return None
    
def get_all_caixa():
    try:
        # Tenta buscar todos os caixas 
        caixas = models.Caixa.select()

        # Verifica se há usuários
        if caixas.exists():
            # Retorna a lista de usuários se houver algum
            return [
                {
                    "idCaixa": str(caixa.idCaixa),
                    "saldoInicial": str(caixa.saldoInicial),
                    "dataAbertura": str(caixa.dataAbertura),
                    "dataFechamento": str(caixa.dataFechamento),
                    "aberto": caixa.aberto,
                    "observacoes": caixa.observacoes,
                    "somenteDinheiro": str(caixa.somenteDinheiro),            
                    "SaldoFinal": str(caixa.saldoFinal)                    
                }

                for caixa in caixas if caixa.aberto == False
               
            ]
        else:
            # Se não houver usuários, retorna None
            return None
    except DoesNotExist:
        # Se ocorrer uma exceção DoesNotExist, retorna None
        return None
    




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
            "dataNascimento": usuario.dataNascimento.isoformat(),
            "cpf": usuario.cpf,
            "endereco": usuario.endereco,
            "telefone": usuario.telefone,
            "cargo": usuario.cargo
        }
    except DoesNotExist:
        return None

def get_cliente(telefone):
    try:
        cliente = models.Cliente.get(models.Cliente.telefone == telefone)

        # Retorna um dicionário contendo apenas atributos não nulos
        return {
            "idCliente": str(cliente.idCliente),
            "email": cliente.email if cliente.email is not None else None,
            "nome": cliente.nome,
            "dataNascimento": cliente.dataNascimento.isoformat() if cliente.dataNascimento is not None else None,
            "cpf": cliente.cpf if cliente.cpf is not None else None,
            "endereco": cliente.endereco if cliente.endereco is not None else None,
            "telefone": cliente.telefone if cliente.telefone is not None else None,
            "saldo": str(cliente.saldo) if cliente.saldo is not None else None
        }

    except DoesNotExist:
        return None

def get_product_by_id(uuid):
    try:
        produto = models.Produto.get(models.Produto.idProduto == uuid)
        return produto
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
    
def get_all_clientes():
    try:
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
                    "dataNascimento": cliente.dataNascimento.isoformat() if cliente.dataNascimento is not None else None,
                    "cpf": cliente.cpf if cliente.cpf is not None else None,
                    "endereco": cliente.endereco if cliente.endereco is not None else None,
                    "telefone": cliente.telefone if cliente.telefone is not None else None,
                    "saldo": str(cliente.saldo) if cliente.saldo is not None else None
                }
                for cliente in clientes
            ]
        else:
            # Se não houver clientes, retorna None
            return None
    except DoesNotExist:
        # Se ocorrer uma exceção DoesNotExist, retorna None
        return None

def get_all_produtos():
    try:
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
                    "categoria": produto.categoria,
                    "valorCusto": str(produto.valorCusto),
                    "valorVenda": str(produto.valorVenda),
                    "unidadeMedida": produto.unidadeMedida,
                    "quantidade": str(produto.quantidade)
                }
                for produto in produtos
            ]
        else:
            # Se não houver produtos, retorna None
            return None
    except DoesNotExist:
        # Se ocorrer uma exceção DoesNotExist, retorna None
        return None

def update_cliente(uuid, telefone=None, email=None, nome=None, dataNascimento=None, cpf=None, endereco=None, saldo=None):
    try:
        cliente = models.Cliente.get(models.Cliente.idCliente == uuid)
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
            "dataNascimento": cliente.dataNascimento.isoformat() if cliente.dataNascimento is not None else None,
            "cpf": cliente.cpf if cliente.cpf is not None else None,
            "endereco": cliente.endereco if cliente.endereco is not None else None,
            "telefone": cliente.telefone if cliente.telefone is not None else None,
            "saldo": str(cliente.saldo) if cliente.saldo is not None else None
        }

    except DoesNotExist:
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
            "dataNascimento": usuario.dataNascimento.isoformat(),
            "cpf": usuario.cpf,
            "endereco": usuario.endereco,
            "telefone": usuario.telefone,
            "cargo": usuario.cargo
        }

    except DoesNotExist:
        return None

def update_novo_saldoInicial(uuid, novoSaldo = None):
    try:

        caixa = models.Caixa.get(models.Caixa.idCaixa == uuid)

        if caixa is None:
            return None
        if novoSaldo is not None:
            caixa.saldoInicial = novoSaldo
        caixa.save()

        return { "saldoInicial": caixa.saldoInicial}
    
    except DoesNotExist:
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
            produto.categoria = categoria
        if valorCusto is not None:
            produto.valorCusto = valorCusto
        if valorVenda is not None:
            produto.valorVenda = valorVenda
        if unidadeMedida is not None:
            produto.unidadeMedida = unidadeMedida

        produto.save()

        return {
            "idProduto": str(produto.idProduto),
            "nome": produto.nome,
            "descricao": produto.descricao if produto.descricao is not None else None,
            "categoria": produto.categoria,
            "valorCusto": str(produto.valorCusto),
            "valorVenda": str(produto.valorVenda),
            "unidadeMedida": produto.unidadeMedida,
            "quantidade": str(produto.quantidade)
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
    
def delete_user(uuid):
    try:
        usuario = models.Usuario.get(models.Usuario.idUsuario == uuid)
        usuario.delete_instance()
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
    
def update_stock_product(uuid, quantidade):
    try:
        produto = models.Produto.get(models.Produto.idProduto == uuid)
        produto.quantidade += Decimal(str(quantidade))
        produto.save()
        return True
    except DoesNotExist:
        return None