import os
import dotenv
from peewee import *

dotenv.load_dotenv()

db_name = os.getenv('DB_NAME')
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_host = os.getenv('DB_HOST')
db_port = os.getenv('DB_PORT')

if db_port:
    db_port = int(db_port)
else:
    db_port = 5432

# Configuração do banco de dados Peewee
db = PostgresqlDatabase(database=db_name, user=db_user, password=db_password, host=db_host, port=db_port)
