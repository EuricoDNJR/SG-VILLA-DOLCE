import logging

from fastapi import APIRouter, Depends, Response, status
from fastapi.responses import JSONResponse
from dependencies import get_token_header
from database.crud.dashboard import (
    categorias_mais_vendidas,
    clientes_que_mais_compraram,
    produtos_mais_vendidos,
    vendas_mensais_do_semestre,
)

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


@router.get(
    "/clients_who_most_purchased/",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(get_token_header)],
)
def get_clients_who_most_purchased():
    """
    Retorna os clientes que mais compraram nos ultimos 6 meses.
    """
    try:
        logging.info("Getting clients who most purchased")
        clientes = clientes_que_mais_compraram()
        if clientes is None:
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        logging.info("Clients who most purchased found")
        return JSONResponse(status_code=status.HTTP_200_OK, content=clientes)
    except Exception as e:
        logging.error(e)
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": "Erro ao buscar clientes que mais compraram"},
        )


@router.get(
    "/top-selling-products/",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(get_token_header)],
)
def top_selling_products():
    """
    Retorna os produtos mais vendidos nos ultimos 6 meses.
    """
    try:
        logging.info("Getting top selling products")
        produtos = produtos_mais_vendidos()
        if produtos is None:
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        logging.info("Top selling products found")
        return JSONResponse(status_code=status.HTTP_200_OK, content=produtos)
    except Exception as e:
        logging.error(e)
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": "Erro ao buscar produtos mais vendidos"},
        )


@router.get(
    "/monthly_sales_of_the_semester/",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(get_token_header)],
)
def monthly_sales_of_the_semester():
    """
    Retorna as vendas mensais do semestre.
    """
    try:
        logging.info("Getting monthly sales of the semester")
        vendas_mensais = vendas_mensais_do_semestre()
        logging.info("Monthly sales of the semester found")
        return JSONResponse(status_code=status.HTTP_200_OK, content=vendas_mensais)
    except Exception as e:
        logging.error(e)
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": "Erro ao buscar vendas mensais do semestre"},
        )
