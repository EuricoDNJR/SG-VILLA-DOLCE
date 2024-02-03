import logging

from fastapi import APIRouter, Depends, Response, status
from fastapi.responses import JSONResponse
from dependencies import get_token_header
from database.crud.dashboard import categorias_mais_vendidas

router = APIRouter()


@router.get(
    "/best-selling-categories/",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(get_token_header)],
)
def get_best_selling_categories():
    """
    Retorna as categorias mais vendidas nos ultimos 6 meses.
    """
    try:
        logging.info("Getting best selling categories")
        categorias = categorias_mais_vendidas()
        if categorias is None:
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        logging.info("Best selling categories found")
        return JSONResponse(status_code=status.HTTP_200_OK, content=categorias)
    except Exception as e:
        logging.error(e)
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": "Erro ao buscar categorias mais vendidas"},
        )
