import os
import dotenv
from peewee import PostgresqlDatabase, SqliteDatabase

dotenv.load_dotenv()

db_engine = os.getenv("DB_ENGINE", "postgres").strip().lower()
db_name = os.getenv("DB_NAME")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")
db_sqlite_path = os.getenv("DB_SQLITE_PATH")

if db_port:
    db_port = int(db_port)
else:
    db_port = 5432


def _resolve_sqlite_path() -> str:
    if db_sqlite_path:
        return db_sqlite_path

    app_data_root = os.getenv("LOCALAPPDATA") or os.getenv("APPDATA") or os.getcwd()
    data_dir = os.path.join(app_data_root, "SG-VILLA-DOLCE", "data")
    os.makedirs(data_dir, exist_ok=True)
    return os.path.join(data_dir, "villa_dolce.db")


if db_engine == "sqlite":
    sqlite_path = _resolve_sqlite_path()
    db = SqliteDatabase(
        sqlite_path,
        pragmas={
            "journal_mode": "wal",
            "foreign_keys": 1,
            "cache_size": -1024 * 64,
            "synchronous": 1,
        },
    )
else:
    db = PostgresqlDatabase(
        database=db_name,
        user=db_user,
        password=db_password,
        host=db_host,
        port=db_port,
    )
