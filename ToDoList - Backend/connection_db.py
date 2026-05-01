import psycopg2 #CONEXAO DO POSTGRE SQL
from psycopg2 import Error
from dotenv import load_dotenv #CORREGAR O AMBIENTE (.ENV)
import os

load_dotenv()

def connection():
    try:
        pwd = os.getenv("POSTGRES_DB_PASSWORD")
        conexao_db = psycopg2.connect(
            user = "postgres",
            password = pwd,
            host = "localhost",
            port = 5432,
            database = "db_todolist")

        print("Conexão realizada com Sucesso!")
        return conexao_db

    except Error:
        print(f"Erro ao tentar conectar ao banco de dados {Error}")

def encerra_connection(conexao):
    if conexao:
        conexao.close()
        print("Conexão encerrada!")

if __name__ == "__main__":   #EXECUTA O CÓDIGO ACIMA. CASO EU IMPORTE ESSA FILE, ELE NÃO EXECUTA DESSA LINHA PARA BAIXO
    connection()
