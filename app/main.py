import logging

logging.basicConfig(
    level=logging.INFO,
    filename="app.log",
    filemode="w",
    format="%(asctime)s - %(levelname)s - %(message)s",
)

if __name__ == "__main__":
    import os
    import dotenv
    import uvicorn

    from fastapi import FastAPI
    from fastapi.middleware.cors import CORSMiddleware
    from contextlib import asynccontextmanager
    from database.dbmain import db
    from database.models import (
        Usuario,
        Pagamento,
        Cliente,
        Caixa,
        Produto,
        Pedido,
        Estoque,
        ProdutoPedido,
        Cargo,
        TipoPagamento,
        Categoria,
    )
    from database.initial_data import create_initial_values
    from routers.v1 import (
        dashboard,
        cliente,
        usuario,
        produto,
        estoque,
        caixa,
        pedido,
        cargo,
        tipo_pagamento,
        categoria,
    )

    dotenv.load_dotenv()

    ENV = os.getenv("ENV")
    api_version = "v0.1.0"

    api_metadata = {
        "title": "Villa Dolce API",
        "description": "API para o sistema de gerenciamento do Açaí Villa Dolce.",
        "version": api_version,
    }

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        # Inicialização do banco de dados
        logging.info("Connecting Database")
        db.connect()
        logging.info("Creating Tables")
        db.create_tables(
            [
                Usuario,
                Pagamento,
                Cliente,
                Caixa,
                Produto,
                Pedido,
                Estoque,
                ProdutoPedido,
                Cargo,
                TipoPagamento,
                Categoria,
            ],
            safe=True,
        )
        logging.info("Tables Created")
        logging.info("Creating Initial Values")
        create_initial_values()
        logging.info("Initial Values Created")
        logging.info("Database Connected")
        yield
        # Desconexão do banco de dados
        logging.info("Shutdown")
        logging.info("Disconnecting Database")
        db.close()
        logging.info("Database Disconnected")

    if ENV == "development":
        print("Development")
        app = FastAPI(
            title=api_metadata["title"],
            description=api_metadata["description"],
            version=api_metadata["version"],
            lifespan=lifespan,
        )
    else:
        app = FastAPI(
            title=api_metadata["title"],
            description=api_metadata["description"],
            version=api_metadata["version"],
            docs_url=None,
            redoc_url=None,
            lifespan=lifespan,
        )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(dashboard.router, prefix="/v1/dashboard", tags=["Dashboard"])
    app.include_router(cliente.router, prefix="/v1/cliente", tags=["Cliente"])
    app.include_router(usuario.router, prefix="/v1/usuario", tags=["Usuario"])
    app.include_router(produto.router, prefix="/v1/produto", tags=["Produto"])
    app.include_router(categoria.router, prefix="/v1/categoria", tags=["Categoria"])
    app.include_router(estoque.router, prefix="/v1/estoque", tags=["Estoque"])
    app.include_router(caixa.router, prefix="/v1/caixa", tags=["Caixa"])
    app.include_router(pedido.router, prefix="/v1/pedido", tags=["Pedido"])
    app.include_router(cargo.router, prefix="/v1/cargo", tags=["Cargo"])
    app.include_router(
        tipo_pagamento.router, prefix="/v1/tipo_pagamento", tags=["Tipo Pagamento"]
    )

    @app.get("/")
    async def root():
        return {"api-version": api_version}

    # Adicione qualquer configuração adicional que você precise
    uvicorn.run(app, host="0.0.0.0", port=8000)
