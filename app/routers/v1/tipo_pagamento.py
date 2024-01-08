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

@router.get("/get_payment_type/{idTipoPagamento}", status_code=status.HTTP_200_OK, dependencies=[Depends(get_token_header)])
def get_PaymentType(idTipoPagamento: str):
    try:
        logging.info("Getting PaymentType")
        tipo_pagamento = crud.get_tipo_pagamento_by_id(idTipoPagamento)
        if tipo_pagamento is None:
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        logging.info("PaymentType found")
        return JSONResponse(status_code=status.HTTP_200_OK, content={"uuid": str(tipo_pagamento.idTipoPagamento), "Nome": tipo_pagamento.nome})
    except Exception as e:
        logging.error(e)
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"message": "Erro ao buscar o tipo_pagamento"})
    
@router.get("/get_all_payment_types", status_code=status.HTTP_200_OK, dependencies=[Depends(get_token_header)])
def get_all_payment_types():
    try:
        logging.info("Getting all PaymentTypes")
        tipo_pagamentos = crud.get_all_tipo_pagamentos()
        if tipo_pagamentos is None:
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        logging.info("PaymentTypes found")
        return JSONResponse(status_code=status.HTTP_200_OK, content=tipo_pagamentos)
    except Exception as e:
        logging.error(e)
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"message": "Erro ao buscar os tipo_pagamentos"})

class UpdatePaymentTypeRequest(BaseModel):
    nome: Optional[str] = None    
@router.patch("/update_PaymentType/{idTipoPagamento}", status_code=status.HTTP_200_OK, dependencies=[Depends(get_token_header)])
def update_PaymentType(idTipoPagamento: str, data: UpdatePaymentTypeRequest):
    try:
        logging.info("Updating PaymentType")
        update_tipo_pagamento = crud.update_tipo_pagamento(idTipoPagamento, data.nome)
        if update_tipo_pagamento:
            logging.info("PaymentType updated")
            return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Tipo de pagamento atualizado com sucesso"})
        else:
            logging.info("PaymentType not updated")
            return Response(status_code=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        logging.error(e)
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"message": "Erro ao atualizar o tipo_pagamento"})
    
# @router.delete("/delete_PaymentType/{idtipo_pagamento}", status_code=status.HTTP_200_OK, dependencies=[Depends(get_token_header)])
# def delete_PaymentType(idtipo_pagamento: str):
#     try:
#         delete_tipo_pagamento = crud.delete_tipo_pagamento(idtipo_pagamento)
#         if delete_tipo_pagamento:
#             logging.info("PaymentType deleted")
#             return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "tipo_pagamento deletado com sucesso"})
#         else:
#             logging.info("PaymentType not deleted")
#             return Response(status_code=status.HTTP_204_NO_CONTENT)
#     except Exception as e:
#         logging.error(e)
#         return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"message": "Erro ao deletar o tipo_pagamento"})