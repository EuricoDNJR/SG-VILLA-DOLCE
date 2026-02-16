from decimal import Decimal
import datetime

from database import models
from database.crud.caixa import update_balance_caixa_pedido
from database.crud.cliente import create_cliente, delete_cliente, update_cliente
from database.crud.pagamento import create_pagamento, delete_pagamento, update_pagamento
from database.crud.pedido import (
    create_pedido,
    delete_pedido,
    delete_produto_pedido,
    delete_replace_quantity_product,
    get_pedido_by_id,
    get_pedido_object_by_id,
    update_balance_client_and_order,
    update_balance_client_and_order_cancel,
    update_pedido_status,
)
from database.crud.produto import (
    create_produto,
    delete_product,
    update_product,
    update_quantity_product,
)
from database.crud.produto_pedido import create_produto_pedido


def _get_entity_id(payload: dict, key: str, fallback: str = None):
    return payload.get(key) or fallback


def _apply_cliente(operation: str, payload: dict, entity_id: str = None):
    if operation == "create":
        existing = None
        if entity_id:
            existing = models.Cliente.get_or_none(models.Cliente.idCliente == entity_id)
        if existing:
            return

        create_cliente(
            payload.get("email"),
            payload.get("nome"),
            payload.get("dataNascimento"),
            payload.get("cpf"),
            payload.get("endereco"),
            payload.get("telefone"),
            payload.get("saldo"),
        )
        return

    target_id = _get_entity_id(payload, "idCliente", entity_id)
    if not target_id:
        raise ValueError("idCliente ausente no evento de cliente")

    if operation == "update":
        updated = update_cliente(
            uuid=target_id,
            telefone=payload.get("telefone"),
            email=payload.get("email"),
            nome=payload.get("nome"),
            dataNascimento=payload.get("dataNascimento"),
            cpf=payload.get("cpf"),
            endereco=payload.get("endereco"),
            saldo=payload.get("saldo"),
        )
        if updated is None:
            raise ValueError("cliente nao encontrado para update")
        return

    if operation == "delete":
        if not delete_cliente(target_id):
            raise ValueError("cliente nao encontrado para delete")
        return

    raise ValueError(f"operacao de cliente nao suportada: {operation}")


def _apply_produto(operation: str, payload: dict, entity_id: str = None):
    if operation == "create":
        existing = None
        if entity_id:
            existing = models.Produto.get_or_none(models.Produto.idProduto == entity_id)
        if existing:
            return

        created = create_produto(
            payload.get("nome"),
            payload.get("descricao"),
            payload.get("categoria"),
            payload.get("valorVenda"),
        )
        if created is None:
            raise ValueError("erro ao criar produto")
        return

    target_id = _get_entity_id(payload, "idProduto", entity_id)
    if not target_id:
        raise ValueError("idProduto ausente no evento de produto")

    if operation == "update":
        updated = update_product(
            uuid=target_id,
            nome=payload.get("nome"),
            descricao=payload.get("descricao"),
            categoria=payload.get("categoria"),
            valorVenda=payload.get("valorVenda"),
            unidadeMedida=payload.get("unidadeMedida"),
        )
        if updated is None:
            raise ValueError("produto nao encontrado para update")
        return

    if operation == "delete":
        if not delete_product(target_id):
            raise ValueError("produto nao encontrado para delete")
        return

    raise ValueError(f"operacao de produto nao suportada: {operation}")


def _apply_pedido_create(payload: dict):
    pagamento_payload = payload.get("Pagamento") or {}
    produtos_payload = payload.get("idProdutos") or []

    pagamento = create_pagamento(
        valorRecebimento=pagamento_payload.get("valorRecebimento", 0.0),
        valorDevolvido=pagamento_payload.get("valorDevolvido", 0.0),
        tipoPagamento=pagamento_payload.get("tipoPagamento"),
    )
    if pagamento is None:
        raise ValueError("erro ao criar pagamento do pedido")

    pedido = create_pedido(
        idCliente=payload.get("idCliente"),
        idPagamento=pagamento.idPagamento,
        idUsuario=payload.get("idUsuario") or payload.get("jwt_token"),
        idCaixa=payload.get("idCaixa"),
        status=payload.get("status"),
        data_criacao=payload.get("data_criacao")
        or payload.get("dataCriacao")
        or datetime.date.today(),
    )
    if pedido is None:
        raise ValueError("erro ao criar pedido")

    for produto in produtos_payload:
        produto_pedido = create_produto_pedido(
            idPedido=pedido.idPedido,
            idProduto=produto.get("idProduto"),
            quantidade=produto.get("quantidade"),
            valorVendaUnd=produto.get("valorVendaUnd"),
            desconto=produto.get("desconto"),
        )

        if produto_pedido.idProduto.categoria.unidadeMedida == "UND":
            pedido.quantidade_produtos_pedido += int(produto.get("quantidade"))
        else:
            pedido.quantidade_produtos_pedido += 1

        update_quantity_product(produto.get("idProduto"), produto.get("quantidade"))

    pedido.save()
    update_balance_client_and_order(pedido)

    if payload.get("status") == "Pago":
        update_balance_caixa_pedido(
            payload.get("idCaixa"),
            pedido.idPagamento.valorTotal,
            pedido.idPagamento.tipoPagamento,
        )


def _apply_pedido_finish(payload: dict, entity_id: str):
    pedido = get_pedido_object_by_id(idPedido=entity_id)
    if pedido is None:
        raise ValueError("pedido nao encontrado para finish")

    if pedido.status == "Pago":
        return

    valor_recebimento = payload.get("valorRecebimento")
    valor_devolvido = payload.get("valorDevolvido", 0.0)
    tipo_pagamento = payload.get("tipoPagamento")

    if (
        Decimal((Decimal(valor_recebimento) - Decimal(valor_devolvido)).__format__(".2f"))
        != pedido.idPagamento.valorTotal
    ):
        raise ValueError("valor recebido menos troco nao confere com total do pedido")

    update_pagamento(
        pedido=pedido,
        valorRecebimento=valor_recebimento,
        valorDevolvido=valor_devolvido,
        tipoPagamento=tipo_pagamento,
    )
    update_balance_caixa_pedido(
        pedido.idCaixa, pedido.idPagamento.valorTotal, pedido.idPagamento.tipoPagamento
    )
    update_pedido_status(pedido, "Pago")


def _apply_pedido_cancel(entity_id: str):
    pedido = get_pedido_object_by_id(idPedido=entity_id)
    if pedido is None:
        raise ValueError("pedido nao encontrado para cancel")

    if pedido.status == "Cancelado":
        return

    update_balance_caixa_pedido(
        pedido.idCaixa,
        -abs(pedido.idPagamento.valorTotal),
        pedido.idPagamento.tipoPagamento,
    )
    update_pagamento(
        pedido=pedido,
        valorRecebimento=0.0,
        valorDevolvido=0.0,
        tipoPagamento="Cancelado",
    )
    update_balance_client_and_order_cancel(pedido)
    delete_replace_quantity_product(pedido.idPedido)
    update_pedido_status(pedido, "Cancelado")


def _apply_pedido_delete(entity_id: str):
    pedido = get_pedido_by_id(idPedido=entity_id)
    if pedido is None:
        return

    if pedido.get("status") != "Cancelado":
        raise ValueError("pedido precisa estar cancelado para delete")

    delete_produto_pedido(pedido["idPedido"])
    delete_pedido(pedido["idPedido"])
    delete_pagamento(pedido["idPagamento"])


def _apply_pedido(operation: str, payload: dict, entity_id: str = None):
    target_id = _get_entity_id(payload, "idPedido", entity_id)

    if operation == "create":
        _apply_pedido_create(payload)
        return
    if operation == "finish":
        if not target_id:
            raise ValueError("idPedido ausente no evento finish")
        _apply_pedido_finish(payload, target_id)
        return
    if operation == "cancel":
        if not target_id:
            raise ValueError("idPedido ausente no evento cancel")
        _apply_pedido_cancel(target_id)
        return
    if operation == "delete":
        if not target_id:
            raise ValueError("idPedido ausente no evento delete")
        _apply_pedido_delete(target_id)
        return

    raise ValueError(f"operacao de pedido nao suportada: {operation}")


def apply_sync_event(entity: str, operation: str, payload: dict, entity_id: str = None):
    if entity == "cliente":
        _apply_cliente(operation, payload, entity_id)
        return
    if entity == "produto":
        _apply_produto(operation, payload, entity_id)
        return
    if entity == "pedido":
        _apply_pedido(operation, payload, entity_id)
        return

    raise ValueError(f"entidade de sync nao suportada: {entity}")
