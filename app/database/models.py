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
    valorRecebimento = DecimalField(max_digits=10, decimal_places=2)
    valorDevolvido = DecimalField(max_digits=10, decimal_places=2)
    tipoPagamento = CharField()

    class Meta:
        table_name = "Pagamento"

class Cliente(BaseModel):
    idCliente = UUIDField(primary_key=True, default=uuid.uuid4)
    email = CharField()
    nome = CharField()
    dataNascimento = DateField()
    cpf = CharField()
    endereco = CharField()
    telefone = CharField()
    saldo = DecimalField()
   
    class Meta:
        table_name = "Cliente"

class Caixa(BaseModel):
    idCaixa = UUIDField(primary_key=True, default=uuid.uuid4)
    saldoInicial = DecimalField()
    dataAbertura = DateField()
    dataFechamento = DateField(null=True)
    observacoes = TextField(null=True)

    class Meta:
            table_name = "Caixa"

class Produto(BaseModel):
    idProduto = UUIDField(primary_key=True, default=uuid.uuid4)
    nome = CharField()
    descricao = TextField()
    quantidade = IntegerField()
    valorCompra = DecimalField()
    valorVenda = DecimalField()
    unidadeMedida = CharField()
    dataVencimento = DateField(null=True)

    class Meta:
        table_name = "Produto"

class Pedido(BaseModel):
    idPedido = UUIDField(primary_key=True, default=uuid.uuid4)
    idCliente = ForeignKeyField(Cliente, backref='pedidos')
    idPagamento = ForeignKeyField(Pagamento, backref='pedidos')
    idUsuario = ForeignKeyField(Usuario, backref='pedidos')
    idProduto = ForeignKeyField(Produto, backref='pedidos')
    idCaixa = ForeignKeyField(Caixa, backref='pedidos')

    class Meta:
        table_name = "Pedido"