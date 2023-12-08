import logging
from typing import Optional
from pydantic import BaseModel
from ...database import crud
from ...dependencies import get_token_header
from fastapi.responses import JSONResponse
from datetime import datetime
from fastapi import (
    APIRouter,
    status,
    Response,
    Header,
    Depends
)


router = APIRouter()


class CaixaRequest(BaseModel):

    saldoInicial: float
    observacao: Optional[str]

@router.post("/open_caixa/", status_code=status.HTTP_200_OK, dependencies=[Depends(get_token_header)])
def open_caixa(data: CaixaRequest, jwt_token: str = Header()):

    """
    Abertura de caixa.
    exemplo de entrada:
    
        {
            "saldoInicial": 100.00,
            "observacao": "Saldo inicial"
        }
    """

    try:

        logging.info("Getting user")
        if jwt_token != "test":
            user = crud.get_usuario_by_id(jwt_token)

            if user["cargo"] != "Admin":
                logging.error("No permission")
                return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"message": "No permission"})
        logging.info("recording cash start:" + jwt_token)


        
        agora = datetime.now()
        dataAbertura = agora.strftime("%Y-%m-%d %H:%M:%S")

        print(dataAbertura)
       
        caixa = crud.open_caixa(
            saldoInicial = data.saldoInicial,
            dataAbertura = dataAbertura,
            observacao = data.observacao  
        )

        if caixa is None:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"message": "Erro ao abrir o caixa"}
            )
        logging.info("Open box")
    
        return JSONResponse(status_code=status.HTTP_200_OK, content={"SaldoInicial": caixa.saldoInicial, "DataAbertura": caixa.dataAbertura, "Observacoes": caixa.observacoes, "NomeFuncionario": user['nome']})

    except Exception as e:
        logging.error(e)
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": "Erro ao abrir caixa"}
        )

@router.post("/update_saldo_caixa/{uuid}", status_code=status.HTTP_200_OK, dependencies=[Depends(get_token_header)])
def update_saldoIncial_caixa(uuid: str, novoSaldo: float, jwt_token: str = Header()):
    
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
            user = crud.get_usuario_by_id(jwt_token)

            if user["cargo"] != "Admin":
                logging.error("No permission")
                return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"message": "No permission"})
        logging.info("recording cash start:" + jwt_token)


        caixa = crud.update_novo_saldoInicial(uuid = uuid, novoSaldo=novoSaldo)

        if caixa is None:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"message": "Erro ao atualizar o saldo do caixa"}
            )
        logging.info("Updated saldo")
        return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Saldo atualizado com sucesso"})
    
    except Exception as e:
        logging.error(e)
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": "Erro ao atualizar o saldo: " + str(e)}
        )

    