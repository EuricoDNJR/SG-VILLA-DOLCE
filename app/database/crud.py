from . import models
from peewee import DoesNotExist
from passlib.hash import bcrypt
from decimal import Decimal
    
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
    
def verifier_client_promotion(pedido):
    if pedido.idCliente.nome != 'Visitante':
        return True
    else:
        return False