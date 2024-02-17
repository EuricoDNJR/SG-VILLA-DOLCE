import logging
from typing import Optional
from pydantic import BaseModel
from database.crud.usuario import get_usuario_by_id
from database.crud.caixa import (
    open_caixa,
    close_caixa,
    update_novo_saldoInicial,
    get_caixa,
    get_caixa_by_id,
    get_all_caixa,
    get_all_paid_and_canceled_orders_caixa,
    get_all_pendent_orders_caixa,
    get_first_caixa_open,
    get_sum_type_payment_by_id,
    get_inputs_outputs_by_id,
)
from dependencies import get_token_header
from fastapi.responses import JSONResponse, Response
from datetime import datetime
from fastapi import APIRouter, status, Header, Depends


router = APIRouter()


class CaixaRequest(BaseModel):
    saldoInicial: float
    observacoes: Optional[str]


@router.post(
    "/open_caixa/",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(get_token_header)],
)
def create_open_caixa(data: CaixaRequest, jwt_token: str = Header()):
    """
    Abertura de caixa.
    exemplo de entrada:

        {
            "saldoInicial": 100.00,
            "observacoes": "Saldo inicial"
        }
    """

    try:
        logging.info("Getting user")
        if jwt_token != "test":
            user = get_usuario_by_id(jwt_token)

        logging.info("recording cash start:" + jwt_token)

        agora = datetime.now()
        dataAbertura = agora.strftime("%Y-%m-%d")
        horaAbertura = agora.strftime("%H:%M:%S")

        caixa = open_caixa(
            saldoInicial=data.saldoInicial,
            dataAbertura=dataAbertura,
            observacoes=data.observacoes,
            horaAbertura=horaAbertura,
            idUsuarioAbertura=jwt_token,
        )

        if caixa is None:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"message": "Erro ao abrir o caixa"},
            )
        logging.info("Open box")

        # retorno com nome do usuario
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "idCaixa": str(caixa.idCaixa),
                "SaldoInicial": caixa.saldoInicial,
                "DataAbertura": caixa.dataAbertura,
                "HoraAbertura": caixa.horaAbertura,
                "Observacoes": caixa.observacoes,
                "NomeFuncionario": user["nome"],
            },
        )

        # return JSONResponse(status_code=status.HTTP_200_OK, content={"uuid": caixa.uuid, "SaldoInicial": caixa.saldoInicial, "DataAbertura": caixa.dataAbertura, "Observacoes": caixa.observacoes})
    except Exception as e:
        logging.error(e)
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": "Erro ao abrir caixa"},
        )


@router.patch(
    "/close_caixa/{idCaixa}",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(get_token_header)],
)
def close_caixa_by_id(idCaixa: str, jwt_token: str = Header()):
    try:
        logging.info("Getting user")
        if jwt_token != "test":
            user = get_usuario_by_id(jwt_token)

        logging.info("recording cash start:" + jwt_token)

        agora = datetime.now()
        dataFechamento = agora.strftime("%Y-%m-%d %H:%M:%S")

        pedidos = get_all_pendent_orders_caixa(idCaixa=idCaixa)
        logging.info("recording cash start:" + jwt_token)

        if pedidos != []:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "message": "O caixa só pode ser fechado quando não houver pedidos em aberto"
                },
            )

        logging.info("Closing caixa")
        caixa = close_caixa(
            uuid=idCaixa, dataFechamento=dataFechamento, idUsuarioFechamento=jwt_token
        )
        if caixa is False:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"message": "Erro ao fechar o caixa"},
            )
        logging.info("Closed caixa")
        logging.info("Updated saldo")

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"message": "Caixa fechado com sucesso"},
        )
    except Exception as e:
        logging.error(e)
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": "Erro ao fechar o caixa: " + str(e)},
        )


class novoSaldo(BaseModel):
    novoSaldo: float


@router.post(
    "/update_saldo_caixa/{idCaixa}",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(get_token_header)],
)
def update_saldoIncial_caixa(data: novoSaldo, uuid: str, jwt_token: str = Header()):
    """
    Atualizar valor inicial .
    exemplo de entrada:

        {
            "novoSaldo": 50.00

        }
    """

    try:
        logging.info("Getting user")
        if jwt_token != "test":
            user = get_usuario_by_id(jwt_token)

            if user["cargo"] != "Admin":
                logging.error("No permission")
                return JSONResponse(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    content={"message": "No permission"},
                )
        logging.info("recording cash start:" + jwt_token)

        caixa = update_novo_saldoInicial(uuid=uuid, novoSaldo=data.novoSaldo)

        if caixa is None:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"message": "Erro ao atualizar o saldo do caixa"},
            )
        logging.info("Updated saldo")
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"message": "Saldo atualizado com sucesso"},
        )

    except Exception as e:
        logging.error(e)
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": "Erro ao atualizar o saldo: " + str(e)},
        )


@router.get(
    "/get_caixa/{date}",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(get_token_header)],
)
def get_caixa_by_date(date: str, jwt_token: str = Header()):
    """
    Buscar caixa por data exata.
    exemplo de entrada:

        {
            "date": "10-12-2023"
        }
    """

    try:
        logging.info("Getting user")
        if jwt_token != "test":
            user = get_usuario_by_id(jwt_token)

            if user["cargo"] != "Admin":
                logging.error("No permission")
                return JSONResponse(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    content={"message": "No permission"},
                )
        logging.info("recording cash start:" + jwt_token)

        date = datetime.strptime(date, "%d-%m-%Y")
        date = date.strftime("%Y-%m-%d")

        caixa = get_caixa(date=date)

        if caixa is None:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"message": "Erro ao pesquisar caixa"},
            )

        """
        caixa_closes = []
        for caixa in caixas:
            
            
            data_invert = datetime.strptime(caixa['dataAbertura'][:10], "%Y-%m-%d")   
            data_invert = data_invert.strftime("%d-%m-%Y")
            if data_invert == data.date and caixa['aberto'] == False:
                caixa_closes.append(caixa)

        if caixa_closes is not None:

            logging.info("Updated saldo")
        """
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "idCaixa": str(caixa.idCaixa),
                "saldoInicial": str(caixa.saldoInicial),
                "dataAbertura": str(caixa.dataAbertura),
                "dataFechamento": str(caixa.dataFechamento),
                "aberto": caixa.aberto,
                "observacoes": caixa.observacoes,
                "somenteDinheiro": str(caixa.somenteDinheiro),
                "SaldoFinal": str(caixa.saldoFinal),
            },
        )
        """
        else:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"message": "Data não consta"}
            )
        """
    except Exception as e:
        logging.error(e)
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": "Erro ao buscar caixa " + str(e)},
        )


@router.get(
    "/get_all_caixa/",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(get_token_header)],
)
def get_all_caixas(jwt_token: str = Header()):
    try:
        logging.info("Getting user")
        if jwt_token != "test":
            user = get_usuario_by_id(jwt_token)

            if user["cargo"] != "Admin":
                logging.error("No permission")
                return JSONResponse(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    content={"message": "No permission"},
                )
        logging.info("recording cash start:" + jwt_token)

        caixas = get_all_caixa()

        if caixas is None:
            return Response(status_code=status.HTTP_204_NO_CONTENT)

        """
        caixa_closes = []
        for caixa in caixas:
            
            
            data_invert = datetime.strptime(caixa['dataAbertura'][:10], "%Y-%m-%d")   
            data_invert = data_invert.strftime("%d-%m-%Y")
            if data_invert == data.date and caixa['aberto'] == False:
                caixa_closes.append(caixa)

        if caixa_closes is not None:

            logging.info("Updated saldo")
        """
        return JSONResponse(status_code=status.HTTP_200_OK, content=caixas)
        """
        else:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"message": "Data não consta"}
            )
        """
    except Exception as e:
        logging.error(e)
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": "Erro ao buscar caixa " + str(e)},
        )


@router.get(
    "/get_all_paid_and_canceled_orders_caixa/{idCaixa}",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(get_token_header)],
)
def get_all_paid_and_canceled_orders_caixas(idCaixa: str, jwt_token: str = Header()):
    try:
        logging.info("Getting user")
        if jwt_token != "test":
            user = get_usuario_by_id(jwt_token)

            if user["cargo"] != "Admin":
                logging.error("No permission")
                return JSONResponse(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    content={"message": "No permission"},
                )
        logging.info("recording cash start:" + jwt_token)
        logging.info("Getting pedidos")
        pedidos = get_all_paid_and_canceled_orders_caixa(idCaixa=idCaixa)
        if pedidos is None:
            logging.error("No pedidos found")
            return Response(status_code=status.HTTP_204_NO_CONTENT)

        return JSONResponse(status_code=status.HTTP_200_OK, content=pedidos)

    except Exception as e:
        logging.error(e)
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": "Erro ao buscar pedidos " + str(e)},
        )


@router.get(
    "/get_all_pendent_orders_caixa/{idCaixa}",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(get_token_header)],
)
def get_all_pendent_orders_caixas(idCaixa: str, jwt_token: str = Header()):
    try:
        logging.info("Getting user")
        if jwt_token != "test":
            user = get_usuario_by_id(jwt_token)

            if user["cargo"] != "Admin":
                logging.error("No permission")
                return JSONResponse(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    content={"message": "No permission"},
                )
        logging.info("recording cash start:" + jwt_token)
        logging.info("Getting pedidos")
        pedidos = get_all_pendent_orders_caixa(idCaixa=idCaixa)
        if pedidos is None:
            logging.error("No pedidos found")
            return Response(status_code=status.HTTP_204_NO_CONTENT)

        return JSONResponse(status_code=status.HTTP_200_OK, content=pedidos)

    except Exception as e:
        logging.error(e)
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": "Erro ao buscar pedidos " + str(e)},
        )


@router.get(
    "/get_first_caixa_open/",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(get_token_header)],
)
def get_first_caixa_op(jwt_token: str = Header()):
    try:
        logging.info("Getting user")
        if jwt_token != "test":
            user = get_usuario_by_id(jwt_token)

            if user["cargo"] != "Admin":
                logging.error("No permission")
                return JSONResponse(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    content={"message": "No permission"},
                )
        logging.info("recording cash start:" + jwt_token)

        caixa = get_first_caixa_open()

        if caixa is None:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"message": "Erro ao pesquisar caixa"},
            )

        return JSONResponse(status_code=status.HTTP_200_OK, content=caixa)

    except Exception as e:
        logging.error(e)
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": "Erro ao buscar caixa " + str(e)},
        )

@router.get("/get_sum_type_payment/{idCaixa}", status_code=status.HTTP_200_OK, dependencies=[Depends(get_token_header)])
def get_sum_type_payment(idCaixa: str, jwt_token: str = Header()):
    try:
        logging.info("Getting user")
        if jwt_token != "test":
            user = get_usuario_by_id(jwt_token)

            if user["cargo"] != "Admin":
                logging.error("No permission")
                return JSONResponse(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    content={"message": "No permission"},
                )
        logging.info("recording cash start:" + jwt_token)

        if get_caixa_by_id(idCaixa) is None:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"message": "Erro ao pesquisar caixa"},
            )

        payment_values = get_sum_type_payment_by_id(idCaixa)
        if payment_values is None:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"message": "Erro ao pesquisar caixa"},
            )

        return JSONResponse(status_code=status.HTTP_200_OK, content=payment_values)
    except Exception as e:
        logging.error(e)
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": "Erro ao buscar caixa " + str(e)},
        )

@router.get("/get_inputs_outputs/{idCaixa}", status_code=status.HTTP_200_OK, dependencies=[Depends(get_token_header)])
def get_inputs_outputs(idCaixa: str, jwt_token: str = Header()):
    try:
        logging.info("Getting user")
        if jwt_token != "test":
            user = get_usuario_by_id(jwt_token)

            if user["cargo"] != "Admin":
                logging.error("No permission")
                return JSONResponse(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    content={"message": "No permission"},
                )
        logging.info("recording cash start:" + jwt_token)

        if get_caixa_by_id(idCaixa) is None:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"message": "Erro ao pesquisar caixa"},
            )

        input_output = get_inputs_outputs_by_id(idCaixa)
        if input_output is None:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"message": "Erro ao pesquisar caixa"},
            )

        return JSONResponse(status_code=status.HTTP_200_OK, content=input_output)
    except Exception as e:
        logging.error(e)
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": "Erro ao buscar caixa " + str(e)},
        )