from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from typing import Optional
from repository_usuarios import criar_usuario, seleciona_usuarios,seleciona_usuario_por_id, atualiza_usuario, deletar_usuario, seleciona_usuario_por_email
from repository_tarefas import create_tarefa, read_tarefas, update_tarefa, delete_tarefa
from connection_db import connection, encerra_connection
from security import hash_senha, verificar_senha, criar_token, validar_token
from jwt.exceptions import InvalidTokenError
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login") #INFORMA AO SWAGGER QUAL A MINHA ROTA DE LOGIN (A QUAL VAI SER GERADA O TOKEN)
#=========================MODELS=========================

class Users(BaseModel):
    nome: str
    email: EmailStr
    senha: str

class Tarefa(BaseModel):
    descricao: str
    status: Optional[str] = "Pendente"

class LoginData(BaseModel):
    email: EmailStr
    senha: str

#=========================HOME=========================

@app.get("/", tags=["Página Inicial"])
def home():
    return {"mensagem": "Minha primeira API"}

#=========================CADASTRO=========================

@app.post("/cadastro", tags=["Cadastro"])
def cadastro_usuario(user: Users):
    conectar = connection()
    cursor = conectar.cursor()

    senha = hash_senha(user.senha)
    criar_usuario(cursor, conectar, user.nome, user.email, senha)
    
    encerra_connection(conectar)
    
    return { # RESPOSTA QUE O FAST API MOSTRA
        "mensagem": "Usuário criado com sucesso",
        "nome": user.nome,
        "email": user.email,
        "senha": senha
    }

#=========================LOGIN=========================

@app.post("/login", tags=["Login"])
def login_usuario(formulario: OAuth2PasswordRequestForm = Depends()): #FORMULÁRIO DE AUTORIZAÇÃO PADRÃO DO FASTAPI, CRIA BOTÃO AUTHORIZE 
    """O OAuth2PasswordRequestForm TEM DOIS CAMPOS PADRÃO: username e password
    USERNAME representa a chave única, pode ser um username, um email, um id específico
    PASSOWORD é a senha criada pelo usuario no ato do registro
    #ANTES DE EXECUTAR O LOGIN, GERA O FORMULÁRIO PADRÃO OAuth2 COM OS CAMPOS username E password"""

    conectar = connection()
    cursor = conectar.cursor()
    
    email_existe = seleciona_usuario_por_email(cursor, formulario.username) #TUPLA ARMAZENADA, O EMAIL DO LOGIN EXISTE NO MEU DB?
    encerra_connection(conectar)

    if email_existe: #SE email_existe NÃO RETORNAR NONE, OU SEJA, RETORNARÁ A TUPLA COM OS DADOS DO USUARIO
        verifica = verificar_senha(formulario.password, email_existe[3]) #VERIFICA SE A SENHA QUE ELE USOU NO LOGIN BATE COM A SENHA HASHEADA NO BANCO
        #email_existe[3] = É A POSIÇÃO DA SENHA NA TUPLA
        if verifica:
            token = criar_token(email_existe[0]) #PASSEI O ID DAQUELE USUARIO
            print(token)
            return {"mensagem": "Usuário conectado!", 
                    "access_token": token, 
                    "token_type": "bearer",
                    "id_usuario": email_existe[0]} # RETORNAR NESSE FORMATO PARA O OAuth2 CONSEGUIR LOCALIZAR O TOKEN e RETORNA TBM PARA O CONSOLE DA WEB
        else:
            return f"Senha incorreta"
    else:
        return f"Email não cadastrado!"


#=========================USERS=========================

@app.get("/users", tags=["Usuários"])
def listar_usuarios():
    conectar = connection() #ESTABELE CONEXAO COM O BANCO DE DADOS
    cursor = conectar.cursor() #OBJETO QUE IRÁ EXECUTAR AS MODIFICAÇÕES NO BANCO DE DADOS

    dados = seleciona_usuarios(cursor)
    encerra_connection(conectar) #ENCERRA CONEXAO COM DB

    #METADE DAS LINHAS DA ROTA SÃO PRA FAZER ITERAÇÃO COM O BANCO E ENVIAR PARA O REPOSITORIO AS INFORMAÇÕES RECEBIDAS PELO SWAGGER DO FASTIAPI. O REPOSITORIO RETORNOU DADOS, POR ISSO A NECESSIDADE DE ATRIBUIR UMA VARIÁVEL PRO RESULTADO DA FUNÇÃO. APENAS ATRIBUO UMA VARIAVEL A FUNÇÃO SE QUERO RECEBER ALGUMA INFORMAÇÃO DELA PARA TRANSMITIR PARA O CLIENTE, CASO NAO QUEIRA, APENAS RETURN OS PARAMETROS DA MINHA QUERY DENTRO DA ROTA ESPECÍFICA DELA

    usuarios = [{"id": u[0], "nome": u[1], "email": u[2], "senha": u[3]} for u in dados] #PRECISA SER CONVERTIDO PARA DICIONARIO (JSON)
    return usuarios


@app.put("/users/{usuario_id}", tags=["Usuários"])
def atualizar_usuario_endpoint(usuario_id: int, user: Users):
    conectar = connection()
    cursor = conectar.cursor()

    # Atualiza o usuário
    atualiza_usuario(cursor, conectar, user.nome, usuario_id)

    # Busca o usuário atualizado via repository
    usuario_att = seleciona_usuario_por_id(cursor, usuario_id)

    encerra_connection(conectar)

    if usuario_att:
        return {"id": usuario_att[0], "nome": usuario_att[1], "email": usuario_att[2]}
    return {"erro": "Usuário não encontrado"}


@app.delete("/users/{usuario_id}", tags=["Usuários"])
def deletar_usuario_endpoint(usuario_id: int):
    conectar = connection()
    cursor = conectar.cursor()

    # Verifica se o usuário existe via repository
    usuario = seleciona_usuario_por_id(cursor, usuario_id)
    if not usuario:
        encerra_connection(conectar)
        return {"erro": "Usuário não encontrado"}

    # Deleta o usuário via repository
    deletar_usuario(cursor, conectar, usuario_id)
    encerra_connection(conectar)

    return {"mensagem": f"Usuário {usuario_id} deletado"}


#=========================TAREFAS=========================

@app.get("/usuarios/{usuario_id}/tarefas", tags=["Tarefas do Usuário"])
def listar_tarefas(usuario_id: int, token_gerado: str = Depends(oauth2_scheme)): 
    """No endpoint, o Depends(oauth2_scheme) diz ao FastAPI:
    "Antes de executar esse endpoint, execute o oauth2_scheme e me entrega o token que ele extraiu do header"
    O oauth2_scheme é uma função que o extrai o token do header e entrega pronto para o seu endpoint.
    OU SEJA, O TOKEN GERADO PELO LOGIN É DADO PELA FUNÇÃO"""
    
    conectar = connection()
    cursor = conectar.cursor()
    
    #Bloco de validação: Valida o token gerado para dar acesso aos endpoints
    if token_gerado is not None:
        try:
            validar_token(token_gerado)
        except InvalidTokenError:
            raise HTTPException(status_code=401, detail="Não foi possível validar. Token inválido ou expirado")
    else:
        raise HTTPException(status_code=401, detail="Usuário deslogado/inativo")
    #fim do bloco

    dados = read_tarefas(cursor, usuario_id)
    encerra_connection(conectar)
    return [{"id_tarefa": t[0], "id_usuario": t[1], "descricao": t[2], "status": t[3]} for t in dados]


@app.post("/usuarios/{usuario_id}/tarefas", tags=["Tarefas do Usuário"])
def criar_tarefa_endpoint(usuario_id: int, tarefa: Tarefa, token_gerado: str = Depends(oauth2_scheme)):

    conectar = connection()
    cursor = conectar.cursor()

    if token_gerado is not None:
        try:
            validar_token(token_gerado)
        except InvalidTokenError:
            raise HTTPException(status_code=401, detail="Não foi possível validar. Token inválido ou expirado")
    else:
        raise HTTPException(status_code=401, detail="Usuário deslogado/inativo")

    id_tarefa = create_tarefa(cursor, conectar, usuario_id, tarefa.descricao, tarefa.status)
    encerra_connection(conectar)

    return {"id_tarefa": id_tarefa, "id_usuario": usuario_id, "descricao": tarefa.descricao, "status": tarefa.status}


@app.put("/usuarios/{usuario_id}/tarefas/{tarefa_id}", tags=["Tarefas do Usuário"])
def atualizar_tarefa_endpoint(usuario_id: int, tarefa_id: int, tarefa: Tarefa, token_gerado: str = Depends(oauth2_scheme)):
    
    conectar = connection()
    cursor = conectar.cursor()

    if token_gerado is not None:
        try:
            validar_token(token_gerado)
        except InvalidTokenError:
            raise HTTPException(status_code=401, detail="Não foi possível validar. Token inválido ou expirado")
    else:
        raise HTTPException(status_code=401, detail="Usuário deslogado/inativo")
    
    update_tarefa(cursor, conectar, usuario_id, tarefa_id, tarefa.descricao, tarefa.status)
    encerra_connection(conectar)
    return {"id_usuario": usuario_id, "id_tarefa": tarefa_id, "descricao": tarefa.descricao, "status": tarefa.status}


@app.delete("/usuarios/{usuario_id}/tarefas/{tarefa_id}", tags=["Tarefas do Usuário"])
def deletar_tarefa_endpoint(usuario_id: int, tarefa_id: int, token_gerado: str = Depends(oauth2_scheme)):

    conectar = connection()
    cursor = conectar.cursor()

    if token_gerado is not None:
        try:
            validar_token(token_gerado)
        except InvalidTokenError:
            raise HTTPException(status_code=401, detail="Não foi possível validar. Token inválido ou expirado")
    else:
        raise HTTPException(status_code=401, detail="Usuário deslogado/inativo")

    delete_tarefa(cursor, conectar, usuario_id, tarefa_id)
    encerra_connection(conectar)
    return {"mensagem": "Tarefa deletada"}

