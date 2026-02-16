# Sistema de Gerenciamento VILLA DOLCE

Aplicacao desktop com Electron (frontend) + FastAPI (backend local embutido), com banco local SQLite e sincronizacao com servidor remoto.

## Arquitetura atual

- Cliente desktop: Electron + Vue + Vuetify
- API local: FastAPI embutida no app (`127.0.0.1:8000`)
- Banco local: SQLite em `%LOCALAPPDATA%/SG-VILLA-DOLCE/data/villa_dolce.db`
- Sync remoto:
  - `push` local -> remoto
  - `pull` remoto -> local
  - monitor a cada 5 segundos quando online

## Fluxo de sincronizacao

- O sistema funciona offline com dados locais.
- Quando ha internet:
  - envia pendencias locais para o servidor remoto
  - busca eventos remotos e aplica localmente
- O sincronismo e eventual (nao e instantaneo em milissegundos).

## Rodar em desenvolvimento (API Python)

### 1. Variaveis de ambiente (`.env`)

Exemplo para Postgres local:

```env
DB_NAME="villa_dolce_db"
DB_USER="postgres"
DB_PASSWORD="root"
DB_HOST="localhost"
DB_PORT=5432
TEST="OFF"
ADMIN_PASSWORD="123"
ENV="development"
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 3. Subir API

```bash
cd app
python main.py
```

## Build do aplicativo Windows (.exe)

Projeto Electron principal:

`frontend/electron-vite-vuetify-app`

### 1. Configurar env embutido do backend local

Arquivo: `builder-local.env`

Exemplo:

```env
DB_ENGINE="sqlite"
DB_SQLITE_PATH=""
DB_SQLITE_CIPHER="OFF"
DB_SQLITE_KEY_FILE=""
TEST="OFF"
ADMIN_PASSWORD="123"
ENV="production"

SYNC_REMOTE_ENABLED="ON"
SYNC_REMOTE_BASE_URL="https://SEU-SERVICO.onrender.com"
SYNC_REMOTE_API_KEY="sua_chave_grande_e_aleatoria"
```

### Opcional: ativar criptografia do banco local (SQLCipher)

No `builder-local.env`:

```env
DB_SQLITE_CIPHER="ON"
DB_SQLITE_KEY_FILE=""
```

Notas:

- `DB_SQLITE_KEY_FILE` vazio usa caminho padrao em `%LOCALAPPDATA%/SG-VILLA-DOLCE/data/sqlite_key.bin`.
- No Windows, a chave e protegida por DPAPI (atrelada ao usuario/machine).
- Se `DB_SQLITE_CIPHER=ON`, a API local precisa das dependencias de SQLCipher.
- Para migrar um `.db` antigo sem criptografia para SQLCipher, gere um novo build e planeje migracao de dados.

### 2. Gerar instalador

```bash
cd frontend/electron-vite-vuetify-app
npm install
npm run build:win
```

Saida em `frontend/electron-vite-vuetify-app/dist`.

## Deploy da API remota

A API remota usa o mesmo codigo do backend (`app/`).

Variaveis recomendadas no servidor:

```env
ENV=production
DB_ENGINE=postgres
DB_HOST=...
DB_PORT=5432
DB_NAME=...
DB_USER=...
DB_PASSWORD=...
TEST=OFF
ADMIN_PASSWORD=...
SYNC_REMOTE_ENABLED=ON
SYNC_REMOTE_BASE_URL=https://SEU-SERVICO.onrender.com
SYNC_REMOTE_API_KEY=sua_chave_grande_e_aleatoria
```

## Verificacao de versao em producao

Endpoints uteis:

- `GET /` -> versao da API
- `GET /version` -> `apiVersion`, `environment`, `gitCommit`, `buildId`

Use isso para confirmar se o deploy remoto esta no commit correto.

## Uso em varios computadores

Sim, o sistema pode operar em varios PCs no estabelecimento.

Para um novo computador, envie:

1. Instalador `.exe` mais recente
2. (Opcional) arquivo SQLite para migrar base local:
   - `%LOCALAPPDATA%/SG-VILLA-DOLCE/data/villa_dolce.db`

Nao precisa Docker no cliente final.

## Troubleshooting rapido

- Erro de sync na tela:
  - o topo do app mostra `Erro sync: ...` com detalhe
- Fila travada:
  - endpoint local `POST /v1/sync/push_pending/` ja reprocessa eventos `processing` antigos
- Se o remoto parecer antigo:
  - confira `GET /version`
  - no provedor, faca deploy com limpeza de cache
