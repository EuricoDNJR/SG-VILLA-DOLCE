import logging
from pydantic import BaseModel
from typing import Optional, List
from ...dependencies import get_token_header
from ...database import crud
from fastapi.responses import JSONResponse
from fastapi import (
    APIRouter,
    status,
    Response,
    Header,
    Depends
)

router = APIRouter()
class CreatePaymentTypeRequest(BaseModel):
    nome: str

@router.post("/create_payment_type", status_code=status.HTTP_201_CREATED, dependencies=[Depends(get_token_header)])
def create_payment_type(data: CreatePaymentTypeRequest):
    try:
        logging.info("Creating Payment Type")
        tipo_pagamento = crud.create_tipo_pagamento(data.nome)
        logging.info("Payment Type created")
        return JSONResponse(status_code=status.HTTP_201_CREATED, content={"uuid": str(tipo_pagamento.idTipoPagamento), "Nome": tipo_pagamento.nome})
    except Exception as e:
        logging.error(e)
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"message": "Erro ao criar o tipo_pagamento"})
