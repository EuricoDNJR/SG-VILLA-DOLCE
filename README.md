![Badge em Desenvolvimento](http://img.shields.io/static/v1?label=STATUS&message=EM%20DESENVOLVIMENTO&color=GREEN&style=for-the-badge)![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)![Electron.js](https://img.shields.io/badge/Electron-191970?style=for-the-badge&logo=Electron&logoColor=white)![Vuetify](https://img.shields.io/badge/Vuetify-1867C0?style=for-the-badge&logo=vuetify&logoColor=AEDDFF)![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)![Poetry](https://img.shields.io/badge/Poetry-%233B82F6.svg?style=for-the-badge&logo=poetry&logoColor=0B3D8D)![Visual Studio Code](https://img.shields.io/badge/Visual%20Studio%20Code-0078d7.svg?style=for-the-badge&logo=visual-studio-code&logoColor=white)![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)![Git](https://img.shields.io/badge/git-%23F05033.svg?style=for-the-badge&logo=git&logoColor=white)![GitHub](https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white)

# Sistema para Gerenciamento VILLA DOLCE

## Descrição

O projeto visa criar um software interno para resolver desafios cruciais enfrentados pelo VILLA DOLCE AÇAÍ. Através do sistema, os usuários poderão melhorar a gestão do estoque, garantindo a disponibilidade constante dos produtos. A automação do controle dos adesivos dos cartões de fidelidade será uma vantagem significativa, assegurando que os clientes sejam recompensados de forma justa e precisa. Por fim, o usuário poderá realizar vendas através do sistema, possibilitando a análise das informações relacionadas às vendas.

## :clipboard: Requisitos para rodar a API

É necessario o .env contendo as tais variáveis de ambiente:
```
DB_NAME = "villa_dolce_db"
DB_USER = "postgres"
DB_PASSWORD = "root"
DB_HOST = "localhost"
DB_PORT = 5432
TEST = "OFF"
ADMIN_PASSWORD = "123"
```

### :heavy_check_mark: Instalação dos requisitos 
A instalação de tais requisitos pode ser feita de duas maneiras:

#### :memo: Utilizando pip e requirements.txt

Crie um arquivo `requirements.txt` e coloque esses packages abaixo:
```
fastapi==0.104.1
uvicorn==0.20.0
peewee==3.16.3
passlib==1.7.4
pydantic==1.10.13
python-dotenv==1.0.0
psycopg2-binary==2.9.9
```

Em seguida execute no terminal:

```
pip install -r requirements.txt
```

#### :gear: Utilizando Poetry

O [Poetry](https://python-poetry.org/) é uma ferramenta de gerenciamento de dependências e empacotamento para projetos Python. Ele simplifica o processo de gerenciamento de dependências, permitindo que você especifique as bibliotecas necessárias para o seu projeto em um arquivo `pyproject.toml` e, em seguida, instale todas as dependências com um único comando.

Dito isso, é bem simples, primeiro instale o Poetry, uma das formas é com o próprio pip, por exemplo:

`pip install poetry`

Vá ao diretório raiz do projeto e em seguida configure o Poetry para criar e gerenciar ambientes virtuais dentro do próprio diretório do projeto:

`poetry config virtualenvs.in-project true`

Depois instale as dependências do projeto listadas no arquivo `pyproject.toml`:

`poetry install`

Por fim, ative o shell dentro do ambiente virtual gerenciado pelo Poetry:

`poetry shell`

### :card_index_dividers: Subindo o banco de dados
Caso queira rodar em um docker-compose:

```
version: '3'
services:
  db:
    image: "postgres:latest"
    container_name: "db"
    ports:
      - "5432:5432"
    environment:
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=root
      - POSTGRES_ROOT_PASSWORD=root
      - POSTGRES_DB=villa_dolce_db
    volumes:
      - ./db:/var/lib/postgresql/data
```

## :computer: Executando a API

Após subir a instância do Banco de Dados por Docker ou local, simplesmente é so executar o `main.py` contido dentro da pasta `app`.

```
python main.py
```

## :mechanical_arm: Transformando a API para .exe (Beta)

Primeiro deve-se instalar a biblioteca [cx-Freeze](https://pypi.org/project/cx-Freeze/):

```pip install cx-Freeze```

Em sequência deverá criar um arquivo chamado `setup.py` no diretório onde o seu `main.py` está, esse arquivo deve conter o seguinte código:

```
from cx_Freeze import setup, Executable

build_exe_options = {
    "packages": ["asyncio", "uvicorn", "fastapi", "contextlib", "database", "routers", "passlib", "pydantic"],
    "include_files": ["app.log"]
}

executables = [
    Executable("main.py", base=None),
]

setup(
    name="Nome do Seu App",
    version="1.0",
    description="Descrição do Seu App",
    options={"build_exe": build_exe_options},
    executables=executables,
)
```

Após a criação do `setup.py` execute o seguinte comando:

```python setup.py build```

Após a construção da aplicação ter finalizado, entre na pasta gerada `build` e la estará o `main.exe`, agora é só executar.

## :monocle_face: Pessoas desenvolvedoras do projeto

| [<img src="https://avatars.githubusercontent.com/u/67143213?v=4" width=115><br><sub>Eurico Júnior</sub>](https://github.com/EuricoDNJR) | [<img src="https://avatars.githubusercontent.com/u/64480492?v=4" width=115><br><sub>Lucas Silva Lopes</sub>](https://github.com/lucassl2020) | [<img src="https://avatars.githubusercontent.com/u/77807221?v=4" width=115><br><sub>Mateus Assis</sub>](https://github.com/MateusVLOs) | [<img src="https://avatars.githubusercontent.com/u/101665939?v=4" width=115><br><sub>Filipe Mateus</sub>](https://github.com/filipe-mateus) | 
| :----------------------------------------------------------------------------------------------------------------------------------------: | :----------------------------------------------------------------------------------------------------------------------------------------------------------: | :---------------------------------------------------------------------------------------------------------------------------------------------: | :-----------------------------------------------------------------------------------------------------------------------------------------------: |