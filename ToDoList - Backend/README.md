# ToDoList API (FastAPI + PostgreSQL)

API de estudo para uma ToDoList com:
- Cadastro e login (OAuth2 Password Flow)
- Senha com hash
- Autenticação via JWT (Bearer Token)
- CRUD de tarefas por usuário

## Stack
- FastAPI + Uvicorn
- PostgreSQL
- psycopg2-binary
- JWT (PyJWT)
- dotenv (`.env`)
- Hash de senha (pwdlib)

## Como rodar (dev)
1. Entre na pasta do backend:
   - `ToDoList - Backend`
2. Crie e ative um ambiente virtual (recomendado).
3. Instale as dependências:
   - `pip install -r requirements.txt`
4. Crie um arquivo `.env` na pasta do backend (veja abaixo).
5. Suba a API:
   - `uvicorn main:app --reload`
6. Swagger (documentação):
   - `http://localhost:8000/docs`

## Variáveis de ambiente (`.env`)
O projeto lê variáveis com `load_dotenv()`:

- `POSTGRES_DB_PASSWORD`  
  Senha do usuário `postgres` do seu Postgres local.

- `SECRET_TOKEN_JWT`  
  Chave secreta usada para assinar/validar os JWTs.

## Banco de dados (PostgreSQL)
A conexão está definida em `connection_db.py` como:
- user: `postgres`
- host: `localhost`
- port: `5432`
- database: `db_todolist`
- password: vem de `POSTGRES_DB_PASSWORD`

## Autenticação (JWT)
- O token é criado em `security.py` com algoritmo `HS256`.
- Expiração padrão: `30` minutos (`ACCESS_TOKEN_EXPIRE_MINUTES`).
- Rotas de tarefas exigem header:
  - `Authorization: Bearer <token>`

## Rotas principais
### Públicas
- `GET /`  
  Retorna mensagem inicial.

- `POST /cadastro`  
  Cria usuário (hash da senha antes de salvar).

- `POST /login`  
  Login via `OAuth2PasswordRequestForm` (campos `username` e `password`).  
  Retorna `access_token`, `token_type` e `id_usuario`.

### Usuários
- `GET /users`  
- `PUT /users/{usuario_id}`  
- `DELETE /users/{usuario_id}`  

### Tarefas (protegidas por token)
- `GET /usuarios/{usuario_id}/tarefas`
- `POST /usuarios/{usuario_id}/tarefas`
- `PUT /usuarios/{usuario_id}/tarefas/{tarefa_id}`
- `DELETE /usuarios/{usuario_id}/tarefas/{tarefa_id}`

## Observações
- O CORS está liberado com `allow_origins=["*"]` (ok para dev; em produção, restrinja ao domínio do frontend).
- O backend usa SQL puro nos repositórios (`repository_usuarios.py` e `repository_tarefas.py`). Usar ORM para evitar isso (ou não).