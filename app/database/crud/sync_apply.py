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


def _resolve_categoria_for_produto(payload: dict):
    requested_categoria = payload.get("categoria") or payload.get("idCategoria")
    categoria_nome = payload.get("categoriaNome")
    unidade_medida = payload.get("unidadeMedida") or "UND"

    if requested_categoria:
        categoria = models.Categoria.get_or_none(
            models.Categoria.idCategoria == requested_categoria
        )
        if categoria is not None:
            return categoria.idCategoria

    if categoria_nome:
        categoria = models.Categoria.get_or_none(models.Categoria.nome == categoria_nome)
        if categoria is not None:
            if unidade_medida and categoria.unidadeMedida != unidade_medida:
                categoria.unidadeMedida = unidade_medida
                categoria.save()
            return categoria.idCategoria

    if requested_categoria:
        try:
            categoria = models.Categoria.create(
                idCategoria=requested_categoria,
                nome=categoria_nome or f"Categoria Sync {str(requested_categoria)[:8]}",
                unidadeMedida=unidade_medida,
            )
            return categoria.idCategoria
        except Exception:
            pass

    categoria = models.Categoria.create(
        nome=categoria_nome or "Categoria Sync",
        unidadeMedida=unidade_medida,
    )
    return categoria.idCategoria


def _resolve_pedido_usuario(payload: dict):
    requested_usuario_id = payload.get("idUsuario") or payload.get("jwt_token")
    if requested_usuario_id:
        usuario = models.Usuario.get_or_none(models.Usuario.idUsuario == requested_usuario_id)
        if usuario is not None:
            return usuario.idUsuario, requested_usuario_id

    admin_usuario = models.Usuario.get_or_none(models.Usuario.cargo == "Admin")
    if admin_usuario is not None:
        return admin_usuario.idUsuario, requested_usuario_id

    any_usuario = models.Usuario.select().first()
    if any_usuario is not None:
        return any_usuario.idUsuario, requested_usuario_id

    raise ValueError("nenhum usuario disponivel no remoto para vincular pedido")


def _resolve_pedido_caixa(payload: dict, fallback_usuario_id):
    requested_caixa_id = payload.get("idCaixa")
    if requested_caixa_id:
        caixa = models.Caixa.get_or_none(models.Caixa.idCaixa == requested_caixa_id)
        if caixa is not None:
            return caixa.idCaixa

        now = datetime.datetime.now()
        caixa = models.Caixa.create(
            idCaixa=requested_caixa_id,
            saldoInicial=0.0,
            dataAbertura=now.date(),
            horaAbertura=now.time().replace(microsecond=0),
            observacoes="Caixa criado automaticamente via sync de pedido",
            aberto=False,
            idUsuarioAbertura=fallback_usuario_id,
            idUsuarioFechamento=fallback_usuario_id,
        )
        return caixa.idCaixa

    caixa_aberto = models.Caixa.get_or_none(models.Caixa.aberto == True)
    if caixa_aberto is not None:
        return caixa_aberto.idCaixa

    caixa_qualquer = models.Caixa.select().first()
    if caixa_qualquer is not None:
        return caixa_qualquer.idCaixa

    now = datetime.datetime.now()
    caixa = models.Caixa.create(
        saldoInicial=0.0,
        dataAbertura=now.date(),
        horaAbertura=now.time().replace(microsecond=0),
        observacoes="Caixa fallback criado automaticamente via sync",
        aberto=False,
        idUsuarioAbertura=fallback_usuario_id,
        idUsuarioFechamento=fallback_usuario_id,
    )
    return caixa.idCaixa


def _apply_cliente(operation: str, payload: dict, entity_id: str = None):
    if operation == "create":
        target_id = _get_entity_id(payload, "idCliente", entity_id)
        existing = None
        if target_id:
            existing = models.Cliente.get_or_none(models.Cliente.idCliente == target_id)

        if existing is None and payload.get("telefone"):
            existing = models.Cliente.get_or_none(
                models.Cliente.telefone == payload.get("telefone")
            )

        # Idempotent behavior for remote sync: if already exists by id/telefone, update.
        if existing is not None:
            update_cliente(
                uuid=str(existing.idCliente),
                telefone=payload.get("telefone"),
                email=payload.get("email"),
                nome=payload.get("nome"),
                dataNascimento=payload.get("dataNascimento"),
                cpf=payload.get("cpf"),
                endereco=payload.get("endereco"),
                saldo=payload.get("saldo"),
            )
        else:
            create_cliente(
                payload.get("email"),
                payload.get("nome"),
                payload.get("dataNascimento"),
                payload.get("cpf"),
                payload.get("endereco"),
                payload.get("telefone"),
                payload.get("saldo"),
                idCliente=target_id,
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
        target_id = _get_entity_id(payload, "idProduto", entity_id)
        resolved_categoria_id = _resolve_categoria_for_produto(payload)
        existing = None
        if target_id:
            existing = models.Produto.get_or_none(models.Produto.idProduto == target_id)

        if existing is None and payload.get("nome"):
            existing = models.Produto.get_or_none(
                models.Produto.nome == payload.get("nome")
            )

        if existing is not None:
            if payload.get("nome") is not None:
                existing.nome = payload.get("nome")
            if payload.get("descricao") is not None:
                existing.descricao = payload.get("descricao")
            if payload.get("valorVenda") is not None:
                existing.valorVenda = payload.get("valorVenda")
            existing.categoria = resolved_categoria_id
            existing.save()
        else:
            created = create_produto(
                payload.get("nome"),
                payload.get("descricao"),
                resolved_categoria_id,
                payload.get("valorVenda"),
                idProduto=target_id,
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


def _apply_pedido_create(payload: dict, entity_id: str = None):
    target_pedido_id = _get_entity_id(payload, "idPedido", entity_id)
    if target_pedido_id:
        existing_pedido = models.Pedido.get_or_none(models.Pedido.idPedido == target_pedido_id)
        if existing_pedido is not None:
            # Idempotent behavior: if the order already exists remotely, treat
            # this create event as already applied.
            return

    pagamento_payload = payload.get("Pagamento") or {}
    produtos_payload = payload.get("idProdutos") or []
    requested_cliente_id = payload.get("idCliente")
    resolved_cliente = (
        models.Cliente.get_or_none(models.Cliente.idCliente == requested_cliente_id)
        if requested_cliente_id
        else None
    )

    # If the order references a client not present remotely yet, try to bootstrap
    # it from snapshot data included in the sync payload.
    if resolved_cliente is None:
        cliente_snapshot = payload.get("clienteSnapshot") or {}
        if cliente_snapshot:
            _apply_cliente(
                "create",
                cliente_snapshot,
                _get_entity_id(cliente_snapshot, "idCliente", requested_cliente_id),
            )
            resolved_cliente = (
                models.Cliente.get_or_none(
                    models.Cliente.idCliente == requested_cliente_id
                )
                if requested_cliente_id
                else None
            )
            if resolved_cliente is None and cliente_snapshot.get("telefone"):
                resolved_cliente = models.Cliente.get_or_none(
                    models.Cliente.telefone == cliente_snapshot.get("telefone")
                )

    if requested_cliente_id and resolved_cliente is None:
        raise ValueError(
            f"cliente do pedido nao encontrado no remoto: idCliente={requested_cliente_id}"
        )

    resolved_usuario_id, _ = _resolve_pedido_usuario(payload)
    resolved_caixa_id = _resolve_pedido_caixa(payload, resolved_usuario_id)
    produtos_snapshot = payload.get("produtosSnapshot") or []
    produtos_snapshot_by_id = {
        str(item.get("idProduto")): item
        for item in produtos_snapshot
        if isinstance(item, dict) and item.get("idProduto")
    }

    pagamento = create_pagamento(
        valorRecebimento=pagamento_payload.get("valorRecebimento", 0.0),
        valorDevolvido=pagamento_payload.get("valorDevolvido", 0.0),
        tipoPagamento=pagamento_payload.get("tipoPagamento"),
    )
    if pagamento is None:
        raise ValueError("erro ao criar pagamento do pedido")

    pedido = create_pedido(
        idCliente=resolved_cliente.idCliente if resolved_cliente else payload.get("idCliente"),
        idPagamento=pagamento.idPagamento,
        idUsuario=resolved_usuario_id,
        idCaixa=resolved_caixa_id,
        status=payload.get("status"),
        data_criacao=payload.get("data_criacao")
        or payload.get("dataCriacao")
        or datetime.date.today(),
        idPedido=target_pedido_id,
    )
    if pedido is None:
        raise ValueError("erro ao criar pedido")

    for produto in produtos_payload:
        produto_id = produto.get("idProduto")
        produto_exists = models.Produto.get_or_none(models.Produto.idProduto == produto_id)
        if produto_exists is None:
            produto_snapshot = produtos_snapshot_by_id.get(str(produto_id))
            if produto_snapshot:
                _apply_produto("create", produto_snapshot, str(produto_id))
            else:
                raise ValueError(
                    f"produto do pedido nao encontrado no remoto: idProduto={produto_id}"
                )

        produto_pedido = create_produto_pedido(
            idPedido=pedido.idPedido,
            idProduto=produto_id,
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
            resolved_caixa_id,
            pedido.idPagamento.valorTotal,
            pedido.idPagamento.tipoPagamento,
        )


def _apply_pedido_finish(payload: dict, entity_id: str):
    pedido = get_pedido_object_by_id(idPedido=entity_id)
    if pedido is None:
        # Idempotent behavior for out-of-order sync: if the order does not
        # exist remotely anymore, treat finish as already applied.
        return

    if pedido.status == "Pago":
        return

    valor_recebimento = Decimal(str(payload.get("valorRecebimento", 0.0)))
    valor_devolvido = Decimal(str(payload.get("valorDevolvido", 0.0)))
    tipo_pagamento = (
        payload.get("tipoPagamento")
        or pedido.idPagamento.tipoPagamento
        or "Dinheiro"
    )

    saldo_recebido = (valor_recebimento - valor_devolvido).quantize(Decimal("0.01"))
    total_pedido = Decimal(str(pedido.idPagamento.valorTotal)).quantize(Decimal("0.01"))

    # For remote sync, prefer eventual consistency over strict rejection:
    # if totals diverge, adjust the received value to match remote order total.
    if saldo_recebido != total_pedido:
        valor_recebimento = (total_pedido + valor_devolvido).quantize(Decimal("0.01"))

    update_pagamento(
        pedido=pedido,
        valorRecebimento=float(valor_recebimento),
        valorDevolvido=float(valor_devolvido),
        tipoPagamento=tipo_pagamento,
    )
    update_balance_caixa_pedido(
        pedido.idCaixa, pedido.idPagamento.valorTotal, pedido.idPagamento.tipoPagamento
    )
    update_pedido_status(pedido, "Pago")


def _apply_pedido_add_items(payload: dict, entity_id: str):
    pedido = get_pedido_object_by_id(idPedido=entity_id)
    if pedido is None:
        raise ValueError("pedido nao encontrado para add_items")

    if pedido.status != "Pendente":
        # Keep operation idempotent if order is already closed/canceled remotely.
        return

    produtos_payload = payload.get("idProdutos") or []
    produtos_snapshot = payload.get("produtosSnapshot") or []
    produtos_snapshot_by_id = {
        str(item.get("idProduto")): item
        for item in produtos_snapshot
        if isinstance(item, dict) and item.get("idProduto")
    }

    for produto in produtos_payload:
        produto_id = produto.get("idProduto")
        produto_exists = models.Produto.get_or_none(models.Produto.idProduto == produto_id)
        if produto_exists is None:
            produto_snapshot = produtos_snapshot_by_id.get(str(produto_id))
            if produto_snapshot:
                _apply_produto("create", produto_snapshot, str(produto_id))
            else:
                raise ValueError(
                    f"produto do add_items nao encontrado no remoto: idProduto={produto_id}"
                )

        produto_instance = create_produto_pedido(
            idPedido=pedido.idPedido,
            idProduto=produto_id,
            quantidade=produto.get("quantidade"),
            valorVendaUnd=produto.get("valorVendaUnd"),
            desconto=produto.get("desconto"),
        )
        update_quantity_product(produto_id, produto.get("quantidade"))
        update_balance_client_and_order_unique(pedido, produto_instance)

        if produto_instance.idProduto.categoria.unidadeMedida == "UND":
            pedido.quantidade_produtos_pedido += int(produto.get("quantidade"))
        else:
            pedido.quantidade_produtos_pedido += 1

    pedido.save()


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
        _apply_pedido_create(payload, target_id)
        return
    if operation == "finish":
        if not target_id:
            raise ValueError("idPedido ausente no evento finish")
        _apply_pedido_finish(payload, target_id)
        return
    if operation == "add_items":
        if not target_id:
            raise ValueError("idPedido ausente no evento add_items")
        _apply_pedido_add_items(payload, target_id)
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
