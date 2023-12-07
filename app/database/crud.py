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

def get_all_estoques_by_product(uuid):
    try:
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
                    "dataEntrada": estoque.dataEntrada.isoformat(),
                    "dataVencimento": estoque.dataVencimento.isoformat() if estoque.dataVencimento is not None else None,
                    "observacoes": estoque.observacoes if estoque.observacoes is not None else None
                }
                for estoque in estoques
            ]
        else:
            # Se não houver registros de estoque, retorna None
            return None
    except DoesNotExist:
        # Se ocorrer uma exceção DoesNotExist, retorna None
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

def get_all_estoques():
    try:
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
                    "dataEntrada": estoque.dataEntrada.isoformat(),
                    "dataVencimento": estoque.dataVencimento.isoformat() if estoque.dataVencimento is not None else None,
                    "observacoes": estoque.observacoes if estoque.observacoes is not None else None
                }
                for estoque in estoques
            ]
        else:
            # Se não houver registros de estoque, retorna None
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

def sum_all_stock_by_product(uuid_product):
    try:
        total = Decimal(0.0)
        estoques = models.Estoque.select().where(models.Estoque.idProduto == uuid_product)
        if estoques.exists():
            for estoque in estoques:
                total += estoque.quantidade
            return total
        else:
            return None
    except DoesNotExist:
        return None
        
def update_stock(idEstoque, idProduto, quantidade=None, dataEntrada=None, dataVencimento=None, observacoes=None):
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
            "dataEntrada": estoque.dataEntrada,
            "dataVencimento": estoque.dataVencimento.isoformat() if estoque.dataVencimento is not None else None,
            "observacoes": estoque.observacoes if estoque.observacoes is not None else None
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
    
def update_stock_product(uuid, quantidade):
    try:
        produto = models.Produto.get(models.Produto.idProduto == uuid)
        produto.quantidade += Decimal(str(quantidade))
        produto.save()
        return True
    except DoesNotExist:
        return None