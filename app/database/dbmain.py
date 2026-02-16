import os
import dotenv
from peewee import PostgresqlDatabase, SqliteDatabase
from security.sqlite_key import get_sqlite_cipher_key

dotenv.load_dotenv()

db_engine = os.getenv("DB_ENGINE", "postgres").strip().lower()
db_name = os.getenv("DB_NAME")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")
db_sqlite_path = os.getenv("DB_SQLITE_PATH")
db_sqlite_cipher = os.getenv("DB_SQLITE_CIPHER", "OFF").strip().upper() == "ON"

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
    sqlite_pragmas = {
        "journal_mode": "wal",
        "foreign_keys": 1,
        "cache_size": -1024 * 64,
        "synchronous": 1,
    }

    if db_sqlite_cipher:
        try:
            from playhouse.sqlcipher_ext import SqlCipherDatabase
        except Exception as import_error:
            raise RuntimeError(
                "DB_SQLITE_CIPHER=ON, mas SQLCipher nao esta disponivel. "
                "Instale dependencias de SQLCipher (ex.: pysqlcipher3/sqlcipher3-binary)."
            ) from import_error

        cipher_key = get_sqlite_cipher_key()
        db = SqlCipherDatabase(
            sqlite_path,
            passphrase=cipher_key,
            pragmas=sqlite_pragmas,
        )
    else:
        db = SqliteDatabase(
            sqlite_path,
            pragmas=sqlite_pragmas,
        )
else:
    db = PostgresqlDatabase(
        database=db_name,
        user=db_user,
        password=db_password,
        host=db_host,
        port=db_port,
    )
