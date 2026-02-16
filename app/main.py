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
    from peewee import OperationalError
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
        SyncQueue,
        SyncCheckpoint,
        SyncInboundEvent,
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
        sync,
    )

    dotenv.load_dotenv()

    ENV = os.getenv("ENV")
    api_version = "v0.1.0"
    build_commit = (
        os.getenv("APP_GIT_COMMIT")
        or os.getenv("RENDER_GIT_COMMIT")
        or "unknown"
    )
    build_id = os.getenv("APP_BUILD_ID") or os.getenv("RENDER_SERVICE_ID") or "unknown"

    api_metadata = {
        "title": "Villa Dolce API",
        "description": "API para o sistema de gerenciamento do Acai Villa Dolce.",
        "version": api_version,
    }

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        # Startup: initialize schema and seed data, then release the connection.
        logging.info(
            "Starting API version=%s env=%s commit=%s build=%s",
            api_version,
            ENV or "unknown",
            build_commit,
            build_id,
        )
        logging.info("Connecting Database")
        db.connect(reuse_if_open=True)
        try:
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
                    SyncQueue,
                    SyncCheckpoint,
                    SyncInboundEvent,
                ],
                safe=True,
            )
            logging.info("Tables Created")
            logging.info("Creating Initial Values")
            create_initial_values()
            logging.info("Initial Values Created")
            logging.info("Database Connected")
        finally:
            if not db.is_closed():
                db.close()

        yield

        logging.info("Shutdown")
        if not db.is_closed():
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

    @app.middleware("http")
    async def db_connection_middleware(request, call_next):
        # Ensure a fresh DB connection per request to avoid stale/closed sessions.
        try:
            db.connect(reuse_if_open=True)
        except OperationalError:
            if not db.is_closed():
                db.close()
            db.connect(reuse_if_open=True)

        try:
            response = await call_next(request)
        finally:
            if not db.is_closed():
                db.close()

        return response

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
    app.include_router(sync.router, prefix="/v1/sync", tags=["Sync"])

    @app.get("/")
    async def root():
        return {"api-version": api_version}

    @app.get("/version")
    async def version():
        return {
            "apiVersion": api_version,
            "environment": ENV or "unknown",
            "gitCommit": build_commit,
            "buildId": build_id,
        }

    uvicorn.run(app, host="0.0.0.0", port=8000)
