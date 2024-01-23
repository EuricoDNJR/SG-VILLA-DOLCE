from . import models
from peewee import DoesNotExist
from passlib.hash import bcrypt
from decimal import Decimal

def create_usuario(email, senha, nome, dataNascimento, cpf, endereco, telefone, cargo):
    return models.Usuario.create(email=email, senha=senha, nome=nome, dataNascimento=dataNascimento, cpf=cpf, endereco=endereco, telefone=telefone, cargo=cargo)

def create_categoria(nome, unidadeMedida):
    return models.Categoria.create(nome=nome, unidadeMedida=unidadeMedida)

def create_produto(nome, descricao, categoria, valorVenda):
    return models.Produto.create(nome=nome, descricao=descricao, categoria=categoria, valorVenda=valorVenda)

def create_estoque(idProduto, quantidade, dataEntrada, dataVencimento, observacoes):
    return models.Estoque.create(idProduto=idProduto, quantidade=quantidade, dataEntrada=dataEntrada, dataVencimento=dataVencimento, observacoes=observacoes)

def create_pagamento(valorRecebimento=0.0, valorDevolvido=0.0, tipoPagamento=None):
    return models.Pagamento.create(valorTotal=Decimal(0.0), valorRecebimento=Decimal(str(valorRecebimento)), valorDevolvido=Decimal(str(valorDevolvido)), tipoPagamento=tipoPagamento)

def create_pedido(idCliente, idPagamento, idUsuario, idCaixa, status):
    return models.Pedido.create(idCliente=idCliente, idPagamento=idPagamento, idUsuario=idUsuario, idCaixa=idCaixa, status=status)

def create_produto_pedido(idPedido, idProduto, quantidade, valorVendaUnd, desconto=0.0):
    return models.ProdutoPedido.create(idPedido=idPedido, idProduto=idProduto, quantidade=quantidade, valorVendaUnd=valorVendaUnd, valorTotal = Decimal(str(valorVendaUnd * quantidade)), desconto=Decimal(str(desconto)))

def create_cargo(nome):
    return models.Cargo.create(nome=nome)

def create_tipo_pagamento(nome):
    return models.TipoPagamento.create(nome=nome)
    
def open_caixa(saldoInicial, dataAbertura, observacoes, horaAbertura, idUsuarioAbertura, idUsuarioFechamento=None):
    return models.Caixa.create(saldoInicial=saldoInicial, dataAbertura=dataAbertura,horaAbertura = horaAbertura, observacoes=observacoes, idUsuarioAbertura=idUsuarioAbertura, idUsuarioFechamento=idUsuarioFechamento)

def close_caixa(uuid, dataFechamento, idUsuarioFechamento):
    try:

        caixa = models.Caixa.get(models.Caixa.idCaixa == uuid)

        if caixa is None:
            return None
        if caixa.aberto == True:
            caixa.dataFechamento = dataFechamento
            caixa.aberto = False
            caixa.idUsuarioFechamento = idUsuarioFechamento
        caixa.save()

        return True
    
    except DoesNotExist:
        return False
    
def get_caixa(date):

    caixa = models.Caixa.get(models.Caixa.dataAbertura == date)

    if caixa.aberto == False:
        return caixa
    else:
        None 
    
def get_all_caixa():
    
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

            for caixa in caixas #if caixa.aberto == False
            
        ]
    else:
        # Se não houver usuários, retorna None
        return None

def get_all_paid_and_canceled_orders_caixa(idCaixa):
    
    pedidos = models.Pedido.select().where(models.Pedido.idCaixa == idCaixa)

    # Verifica se há pedidos
    if pedidos.exists():
        # Retorna a lista de pedidos pagos ou pendentes se houver algum
        return [
                { 
                "idPedido": str(pedido.idPedido),
                "idCliente": str(pedido.idCliente.idCliente),
                "nomeCliente": pedido.idCliente.nome,
                "telefoneCliente": pedido.idCliente.telefone,
                "idPagamento": str(pedido.idPagamento.idPagamento),
                "valorTotal": str(pedido.idPagamento.valorTotal),
                "valorRecebimento": str(pedido.idPagamento.valorRecebimento),
                "valorDevolvido": str(pedido.idPagamento.valorDevolvido),
                "tipoPagamento": pedido.idPagamento.tipoPagamento,
                "idUsuario": str(pedido.idUsuario.idUsuario),
                "nomeUsuario": pedido.idUsuario.nome,
                "idCaixa": str(pedido.idCaixa.idCaixa),
                "status": pedido.status
                } for pedido in pedidos if pedido.status == 'Pago' or pedido.status == 'Cancelado'
            ]
    else:
        # Se não houver pedidos, retorna None
        return None

def get_all_pendent_orders_caixa(idCaixa):
        
        pedidos = models.Pedido.select().where(models.Pedido.idCaixa == idCaixa)
        
        # Retorna a lista de pedidos pagos ou pendentes se houver algum
        return [
                { 
                "idPedido": str(pedido.idPedido),
                "idCliente": str(pedido.idCliente.idCliente),
                "nomeCliente": pedido.idCliente.nome,
                "telefoneCliente": pedido.idCliente.telefone,
                "idPagamento": str(pedido.idPagamento.idPagamento),
                "valorTotal": str(pedido.idPagamento.valorTotal),
                "valorRecebimento": str(pedido.idPagamento.valorRecebimento),
                "valorDevolvido": str(pedido.idPagamento.valorDevolvido),
                "tipoPagamento": pedido.idPagamento.tipoPagamento,
                "idUsuario": str(pedido.idUsuario.idUsuario),
                "nomeUsuario": pedido.idUsuario.nome,
                "idCaixa": str(pedido.idCaixa.idCaixa),
                "status": pedido.status
                } for pedido in pedidos if pedido.status == 'Pendente'
            ]
    
def get_first_caixa_open():
    try:
        caixa = models.Caixa.select().where(models.Caixa.aberto == True).get()
        return {"idCaixa": str(caixa.idCaixa),
                "saldoInicial": str(caixa.saldoInicial),
                "dataAbertura": str(caixa.dataAbertura),
                "dataFechamento": str(caixa.dataFechamento),
                "aberto": caixa.aberto,
                "observacoes": caixa.observacoes,
                "somenteDinheiro": str(caixa.somenteDinheiro),            
                "SaldoFinal": str(caixa.saldoFinal)                    
                }
    except DoesNotExist:
        return None

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

def get_product_by_id(uuid):
    try:
        produto = models.Produto.get(models.Produto.idProduto == uuid)
        return produto
    except DoesNotExist:
        return None

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
                "dataVencimento": str(estoque.dataVencimento) if estoque.dataVencimento is not None else None,
                "observacoes": estoque.observacoes if estoque.observacoes is not None else None
            }
            for estoque in estoques
        ]
    else:
        # Se não houver registros de estoque, retorna None
        return None

def get_pedido_by_id(idPedido):
    try:
        pedido = models.Pedido.get(models.Pedido.idPedido == idPedido)

        return {
            "idPedido": str(pedido.idPedido),
            "idCliente": str(pedido.idCliente.idCliente),
            "nomeCliente": pedido.idCliente.nome,
            "telefoneCliente": pedido.idCliente.telefone,
            "saldoCliente": str(pedido.idCliente.saldo),
            "idPagamento": str(pedido.idPagamento.idPagamento),
            "valorTotal": str(pedido.idPagamento.valorTotal),
            "valorRecebimento": str(pedido.idPagamento.valorRecebimento),
            "valorDevolvido": str(pedido.idPagamento.valorDevolvido),
            "tipoPagamento": pedido.idPagamento.tipoPagamento,
            "idUsuario": str(pedido.idUsuario.idUsuario),
            "nomeUsuario": pedido.idUsuario.nome,
            "idCaixa": str(pedido.idCaixa.idCaixa),
            "status": pedido.status,
            "idProdutos": get_all_produtos_pedidos_by_id(idPedido)
        }
    except DoesNotExist:
        return None

def get_pedido_object_by_id(idPedido):
    try:
        pedido = models.Pedido.get(models.Pedido.idPedido == idPedido)

        return pedido
    except DoesNotExist:
        return None

def get_cargo_by_id(uuid):
    try:
        cargo = models.Cargo.get(models.Cargo.idCargo == uuid)

        return cargo
    except DoesNotExist:
        return None

def get_categoria_by_id(uuid):
    try:
        categoria = models.Categoria.get(models.Categoria.idCategoria == uuid)

        return categoria
    except DoesNotExist:
        return None

def get_tipo_pagamento_by_id(uuid):
    try:
        tipo_pagamento = models.TipoPagamento.get(models.TipoPagamento.idTipoPagamento == uuid)

        return tipo_pagamento
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
                "unidadeMedida": categoria.unidadeMedida
            }
            for categoria in categorias
        ]
    else:
        # Se não houver categorias, retorna None
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
                "dataVencimento": str(estoque.dataVencimento) if estoque.dataVencimento is not None else None,
                "observacoes": estoque.observacoes if estoque.observacoes is not None else None
            }
            for estoque in estoques
        ]
    else:
        # Se não houver registros de estoque, retorna None
        return None

def get_all_pedidos():
    # Tenta buscar todos os pedidos
    pedidos = models.Pedido.select()

    # Verifica se há pedidos
    if pedidos.exists():
        # Retorna a lista de pedidos se houver algum
        return [
            {
                "idPedido": str(pedido.idPedido),
                "idCliente": str(pedido.idCliente.idCliente),
                "nomeCliente": pedido.idCliente.nome,
                "telefoneCliente": pedido.idCliente.telefone,
                "idPagamento": str(pedido.idPagamento.idPagamento),
                "valorTotal": str(pedido.idPagamento.valorTotal),
                "valorRecebimento": str(pedido.idPagamento.valorRecebimento),
                "valorDevolvido": str(pedido.idPagamento.valorDevolvido),
                "tipoPagamento": pedido.idPagamento.tipoPagamento,
                "idUsuario": str(pedido.idUsuario.idUsuario),
                "nomeUsuario": pedido.idUsuario.nome,
                "idCaixa": str(pedido.idCaixa.idCaixa),
                "status": pedido.status,
            }
            for pedido in pedidos
        ]
    else:
        # Se não houver pedidos, retorna None
        return None

def get_all_pedidos_pendentes():
    # Tenta buscar todos os pedidos
    pedidos = models.Pedido.select()

    # Verifica se há pedidos
    if pedidos.exists():
        # Retorna a lista de pedidos se houver algum
        return [
            {
                "idPedido": str(pedido.idPedido),
                "idCliente": str(pedido.idCliente.idCliente),
                "nomeCliente": pedido.idCliente.nome,
                "telefoneCliente": pedido.idCliente.telefone,
                "idPagamento": str(pedido.idPagamento.idPagamento),
                "valorTotal": str(pedido.idPagamento.valorTotal),
                "valorRecebimento": str(pedido.idPagamento.valorRecebimento),
                "valorDevolvido": str(pedido.idPagamento.valorDevolvido),
                "tipoPagamento": pedido.idPagamento.tipoPagamento,
                "idUsuario": str(pedido.idUsuario.idUsuario),
                "nomeUsuario": pedido.idUsuario.nome,
                "idCaixa": str(pedido.idCaixa.idCaixa),
                "status": pedido.status,
            }
            for pedido in pedidos if pedido.status == 'Pendente'
        ]
    else:
        # Se não houver pedidos, retorna None
        return None

def get_all_pedidos_pagos_cancelados():
    # Tenta buscar todos os pedidos
    pedidos = models.Pedido.select()

    # Verifica se há pedidos
    if pedidos.exists():
        # Retorna a lista de pedidos se houver algum
        return [
            {
                "idPedido": str(pedido.idPedido),
                "idCliente": str(pedido.idCliente.idCliente),
                "nomeCliente": pedido.idCliente.nome,
                "telefoneCliente": pedido.idCliente.telefone,
                "idPagamento": str(pedido.idPagamento.idPagamento),
                "valorTotal": str(pedido.idPagamento.valorTotal),
                "valorRecebimento": str(pedido.idPagamento.valorRecebimento),
                "valorDevolvido": str(pedido.idPagamento.valorDevolvido),
                "tipoPagamento": pedido.idPagamento.tipoPagamento,
                "idUsuario": str(pedido.idUsuario.idUsuario),
                "nomeUsuario": pedido.idUsuario.nome,
                "idCaixa": str(pedido.idCaixa.idCaixa),
                "status": pedido.status,
            }
            for pedido in pedidos if pedido.status == 'Pago' or pedido.status == 'Cancelado'
        ]
    else:
        # Se não houver pedidos, retorna None
        return None

def get_all_tipo_pagamentos():
    tipo_pagamentos = models.TipoPagamento.select()

    # Verifica se há tipo_pagamentos
    if tipo_pagamentos.exists():
        # Retorna a lista de tipo_pagamentos se houver algum
        return [
            {
                "idTipoPagamento": str(tipo_pagamento.idTipoPagamento),
                "nome": tipo_pagamento.nome
            }
            for tipo_pagamento in tipo_pagamentos
        ]
    else:
        # Se não houver tipo_pagamentos, retorna None
        return None

def get_all_produtos_pedidos_by_id(idPedido):
    produtos_pedidos = models.ProdutoPedido.select().where(models.ProdutoPedido.idPedido == idPedido)

    # Verifica se há produtos_pedidos
    if produtos_pedidos.exists():
        # Retorna a lista de produtos_pedidos se houver algum
        return [
            {
                "idProdutoPedido": str(produto_pedido.idProdutoPedido),
                "idProduto": str(produto_pedido.idProduto.idProduto),
                "nome": produto_pedido.idProduto.nome,
                "quantidade": str(produto_pedido.quantidade),
                "desconto": str(produto_pedido.desconto),
                "valorVendaUnd": str(produto_pedido.valorVendaUnd),
                "valorTotal": str(produto_pedido.valorTotal)
            }
            for produto_pedido in produtos_pedidos
        ]
    else:
        # Se não houver produtos_pedidos, retorna None
        return None

def update_balance_client_and_order(pedido):
    produtos_pedidos = models.ProdutoPedido.select().where(models.ProdutoPedido.idPedido == pedido.idPedido)

    # Verifica se há produtos_pedidos
    if produtos_pedidos.exists():
        # Verifica se nos produtos do pedido há algum com a categoria Açaí para contabilizar no saldo do cliente
        for produto_pedido in produtos_pedidos:
            if produto_pedido.idProduto.categoria.nome == 'Açaí' and verifier_client_promotion(pedido):
                if produto_pedido.desconto > Decimal(0.0):
                    pedido.idCliente.saldo -= Decimal(150)
                    if produto_pedido.valorTotal < Decimal(15):
                        pedido.idCliente.saldo += Decimal(15) - produto_pedido.desconto
                    produto_pedido.valorTotal -= produto_pedido.desconto
                    produto_pedido.save() 
                    pedido.idCliente.saldo += produto_pedido.valorTotal
                    pedido.idPagamento.valorTotal += produto_pedido.valorTotal
                else:    
                    pedido.idCliente.saldo += produto_pedido.valorTotal
                    pedido.idPagamento.valorTotal += produto_pedido.valorTotal
                pedido.idCliente.save()
                pedido.idPagamento.save()
            else:
                #Se for visitante, não contabiliza o saldo do cliente
                pedido.idPagamento.valorTotal += produto_pedido.valorTotal
                pedido.idPagamento.save()
        return True
    else:
        # Se não houver produtos_pedidos, retorna None
        return None

def update_balance_client_and_order_unique(pedido, produto_instance):
    try:
        if produto_instance.idProduto.categoria.nome == 'Açaí' and verifier_client_promotion(pedido):
            if produto_instance.desconto > Decimal(0.0):
                pedido.idCliente.saldo -= Decimal(150)
                if produto_instance.valorTotal < Decimal(15):
                    pedido.idCliente.saldo += Decimal(15) - produto_instance.desconto
                produto_instance.valorTotal -= produto_instance.desconto
                produto_instance.save() 
                pedido.idCliente.saldo += produto_instance.valorTotal
                pedido.idPagamento.valorTotal += produto_instance.valorTotal
            else:  
                pedido.idCliente.saldo += produto_instance.valorTotal
                pedido.idPagamento.valorTotal += produto_instance.valorTotal
            pedido.idCliente.save()
            pedido.idPagamento.save()
        else:
            #Se for visitante, não contabiliza o saldo do cliente
            pedido.idPagamento.valorTotal += produto_instance.valorTotal
            pedido.idPagamento.save()
        return True
    except DoesNotExist:
        # Se ocorrer uma exceção DoesNotExist, retorna None
        return None

def update_balance_client_and_order_cancel(pedido):
    produtos_pedidos = models.ProdutoPedido.select().where(models.ProdutoPedido.idPedido == pedido.idPedido)

    # Verifica se há produtos_pedidos
    if produtos_pedidos.exists():
        # Verifica se nos produtos do pedido há algum com a categoria Açaí para contabilizar no saldo do cliente
        for produto_pedido in produtos_pedidos:
            if produto_pedido.idProduto.categoria.nome == 'Açaí' and verifier_client_promotion(pedido):
                if produto_pedido.desconto > Decimal(0.0):
                    pedido.idCliente.saldo += Decimal(150)
                    produto_pedido.valorTotal += produto_pedido.desconto
                    produto_pedido.save()
                    pedido.idCliente.saldo -= Decimal(15) - produto_pedido.desconto
                    if produto_pedido.valorTotal > Decimal(15):
                        pedido.idCliente.saldo -= produto_pedido.valorTotal - Decimal(15)
                    pedido.idPagamento.valorTotal -= produto_pedido.valorTotal
                    pedido.idPagamento.save()
                else:    
                    pedido.idCliente.saldo -= produto_pedido.valorTotal
                    pedido.idPagamento.valorTotal -= produto_pedido.valorTotal
                    pedido.idPagamento.save()
                pedido.idCliente.save()
            else:
                #Se for visitante ou ate mesmo produto normal, so decrementa do valor total do pedido
                pedido.idPagamento.valorTotal -= produto_pedido.valorTotal
                pedido.idPagamento.save()
        return True
    else:
        # Se não houver produtos_pedidos, retorna None
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
            "unidadeMedida": categoria.unidadeMedida
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

def update_quantity_product(uuid, quantidade):
    try:
        produto = models.Produto.get(models.Produto.idProduto == uuid)
        produto.quantidade -= Decimal(str(quantidade))
        produto.save()
        return True
    except DoesNotExist:
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
            "dataEntrada": str(estoque.dataEntrada),
            "dataVencimento": str(estoque.dataVencimento) if estoque.dataVencimento is not None else None,
            "observacoes": estoque.observacoes if estoque.observacoes is not None else None
        }

    except DoesNotExist:
        return None

def update_balance_caixa_pedido(idCaixa, valorTotal, tipoPagamento):
    try:
        caixa = models.Caixa.get(models.Caixa.idCaixa == idCaixa)
        caixa.saldoFinal += valorTotal
        caixa.save()
        if tipoPagamento == 'Dinheiro':
            caixa.somenteDinheiro += valorTotal
            caixa.save()
        return True
    except DoesNotExist:
        return None

def update_pagamento(pedido, tipoPagamento, valorRecebimento=0.0, valorDevolvido=0.0):
    try:
        pedido.idPagamento.valorRecebimento = Decimal(str(valorRecebimento))
        pedido.idPagamento.valorDevolvido = Decimal(str(valorDevolvido))
        pedido.idPagamento.tipoPagamento = tipoPagamento
        pedido.idPagamento.save()
        return True
    except DoesNotExist:
        return None

def update_pagamento_valorTotal(idPagamento, valorTotalProduto):
    try:
        idPagamento.valorTotal += valorTotalProduto
        idPagamento.save()
        return True
    except DoesNotExist:
        return None

def update_pedido_status(pedido, status):
    try:
        pedido.status = status
        pedido.save()
        return True
    except DoesNotExist:
        return None

def update_pedido_desconto(pedido, desconto):
    try:
        pedido.desconto = desconto
        pedido.save()
        return True
    except DoesNotExist:
        return None

def update_tipo_pagamento(uuid, nome=None):
    try:
        tipo_pagamento = models.TipoPagamento.get(models.TipoPagamento.idTipoPagamento == uuid)
        if tipo_pagamento is None:
            return None
        # Atualiza os atributos fornecidos
        if nome is not None:
            tipo_pagamento.nome = nome

        tipo_pagamento.save()

        return {
            "idTipoPagamento": str(tipo_pagamento.idTipoPagamento),
            "nome": tipo_pagamento.nome
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

def delete_categoria(uuid):
    try:
        categoria = models.Categoria.get(models.Categoria.idCategoria == uuid)
        categoria.delete_instance()
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

def delete_replace_quantity_product(idPedido):
    produtos_pedidos = models.ProdutoPedido.select().where(models.ProdutoPedido.idPedido == idPedido)
    if produtos_pedidos.exists():
        for produto_pedido in produtos_pedidos:
            produto = get_product_by_id(produto_pedido.idProduto.idProduto)
            produto.quantidade += produto_pedido.quantidade
            produto.save()
        return True
    else:
        return None

def delete_produto_pedido(idPedido):
    produtos_pedidos = models.ProdutoPedido.select().where(models.ProdutoPedido.idPedido == idPedido)
    if produtos_pedidos.exists():
        for produto_pedido in produtos_pedidos:
            produto_pedido.delete_instance()
        return True
    else:
        return None

def delete_pagamento(idPagamento):
    try:
        pagamento = models.Pagamento.get(models.Pagamento.idPagamento == idPagamento)
        pagamento.delete_instance()
        return True
    except DoesNotExist:
        return None

def delete_pedido(idPedido):
    try:
        pedido = models.Pedido.get(models.Pedido.idPedido == idPedido)
        pedido.delete_instance()
        return True
    except DoesNotExist:
        return None

def delete_cargo(uuid):
    try:
        cargo = models.Cargo.get(models.Cargo.idCargo == uuid)
        cargo.delete_instance()
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

def delete_payment_type(uuid):
    try:
        tipo_pagamento = models.TipoPagamento.get(models.TipoPagamento.idTipoPagamento == uuid)
        tipo_pagamento.delete_instance()
        return True
    except DoesNotExist:
        return None
    
def verifier_client_promotion(pedido):
    if pedido.idCliente.nome != 'Visitante':
        return True
    else:
        return False