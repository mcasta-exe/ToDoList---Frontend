from pwdlib import PasswordHash
from dotenv import load_dotenv
import os
import jwt
from datetime import datetime, timedelta, timezone

load_dotenv()

#=============================== HASH ============================#

password_hash = PasswordHash.recommended() #Cria o hash. Usar recommended para não precisar criar a salt

def hash_senha(senha):
    return password_hash.hash(senha) #converte a senha em hash

def verificar_senha(senha, hash_salvo):
    verifica = password_hash.verify(senha, hash_salvo) #verifica se a hash inserida no login confere com a do banco
    return verifica


#=============================== JWT ============================#
SECRET_KEY = os.getenv("SECRET_TOKEN_JWT")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30



def criar_token(id, tempo_sessao: timedelta | None=None): # | None = None significa que é OPCIONAL passar o tempo_sessão, caso não passe, cai no else
    payload = {"id": id} #ID DO USUÁRIO
    if tempo_sessao: #CASO QUEIRA PERSONALIZAR UM TEMPO DE SESSÃO
        expirar = datetime.now(timezone.utc) + tempo_sessao
    else:
        expirar = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES) #TEMPO DEFAULT DA SESSÃO
    payload.update({'exp':expirar})
    jwt_codificado = jwt.encode(payload, key=SECRET_KEY, algorithm=ALGORITHM) #JWT É COMPOSTO POR PAYLOAD e SECRET, A HEADER É GERADA PELA FUNÇÃO 
    #EU PODERIA PASSAR OS PARAMETROS DIRETO, MAS FICOU MAIS DIDÁTICO ASSIM
    return jwt_codificado


def validar_token(token):
    print(token)
    jwt_decodificado = jwt.decode(token, key=SECRET_KEY, algorithms=[ALGORITHM])
    return jwt_decodificado