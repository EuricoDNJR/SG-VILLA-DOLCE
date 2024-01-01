import datetime
import uuid
from peewee import *

from .dbmain import db

class BaseModel(Model):
    class Meta:
        database = db

class Usuario(BaseModel):
    idUsuario = UUIDField(primary_key=True, default=uuid.uuid4)
    email = CharField(unique=True)
    nome = CharField()
    dataNascimento = DateField()
    cpf = CharField(unique=True)
    endereco = CharField()
    telefone = CharField(unique=True)
    cargo = CharField()
    senha = CharField()

    class Meta:
        table_name = "Usuario"


class Pagamento(BaseModel):
    idPagamento = UUIDField(primary_key=True, default=uuid.uuid4)
    valorTotal = DecimalField(max_digits=10, decimal_places=2)
    valorRecebimento = DecimalField(max_digits=10, decimal_places=2, default=0.0)
    valorDevolvido = DecimalField(max_digits=10, decimal_places=2, default=0.0)
    tipoPagamento = CharField(null=True)

    class Meta:
        table_name = "Pagamento"

class Cliente(BaseModel):
    idCliente = UUIDField(primary_key=True, default=uuid.uuid4)
    email = CharField(unique=True, null=True)
    nome = CharField()
    dataNascimento = DateField(null=True)
    cpf = CharField(unique=True, null=True)
    endereco = CharField(null=True)
    telefone = CharField(unique=True)
    saldo = DecimalField(decimal_places=2, null=True, default=0.0)
   
    class Meta:
        table_name = "Cliente"

class Caixa(BaseModel):
    idCaixa = UUIDField(primary_key=True, default=uuid.uuid4)
    saldoInicial = DecimalField()
    dataAbertura = DateField()
    horaAbertura = TimeField()
    dataFechamento = DateTimeField(null=True)
    observacoes = TextField(null=True)
    aberto = BooleanField(default=True)
    somenteDinheiro = DecimalField(max_digits=10, decimal_places=2, default=0.0)
    saldoFinal = DecimalField(max_digits=10, decimal_places=2, default=0.0)

    class Meta:
            table_name = "Caixa"

class Produto(BaseModel):
    idProduto = UUIDField(primary_key=True, default=uuid.uuid4)
    nome = CharField(unique=True)
    descricao = TextField(null=True)
    categoria = CharField()
    valorCusto = DecimalField()
    valorVenda = DecimalField()
    unidadeMedida = CharField()
    quantidade = DecimalField(max_digits=10, decimal_places=3, default=0.0)

    class Meta:
        table_name = "Produto"

class Estoque(BaseModel):
    idEstoque = UUIDField(primary_key=True, default=uuid.uuid4)
    idProduto = ForeignKeyField(Produto, backref='estoque')
    quantidade = DecimalField(max_digits=10, decimal_places=3, default=0.0)
    dataEntrada = DateField()
    dataVencimento = DateField(null=True)
    observacoes = TextField(null=True)

    class Meta:
        table_name = "Estoque"

class Pedido(BaseModel):
    idPedido = UUIDField(primary_key=True, default=uuid.uuid4)
    idCliente = ForeignKeyField(Cliente, backref='pedido')
    idPagamento = ForeignKeyField(Pagamento, backref='pedido')
    idUsuario = ForeignKeyField(Usuario, backref='pedido')
    idCaixa = ForeignKeyField(Caixa, backref='pedido')
    status = CharField()

    class Meta:
        table_name = "Pedido"

class ProdutoPedido(BaseModel):
    idProdutoPedido = UUIDField(primary_key=True, default=uuid.uuid4)
    idPedido = ForeignKeyField(Pedido, backref='produtos_pedidos')
    idProduto = ForeignKeyField(Produto, backref='produtos_pedidos')
    quantidade = DecimalField(max_digits=10, decimal_places=3, default=0.0)

    class Meta:
        table_name = "ProdutoPedido"

class Cargo(BaseModel):
    idCargo = UUIDField(primary_key=True, default=uuid.uuid4)
    nome = CharField(unique=True)

    class Meta:
        table_name = "Cargo"