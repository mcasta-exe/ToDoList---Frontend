def criar_usuario(cursor, conectar, nome, email, senha):
    """Insere um novo usuário"""
    comando_sql = "INSERT INTO usuarios (nome, email, senha) VALUES (%s, %s, %s)"
    valores = (nome, email, senha)
    cursor.execute(comando_sql, valores)
    conectar.commit()


def seleciona_usuarios(cursor):
    """Lista todos os usuários"""
    comando_sql = "SELECT * FROM usuarios ORDER BY id ASC" # ID ASCENDENTE
    cursor.execute(comando_sql)
    return cursor.fetchall() #RETORNA UMA TUPLA COM TODOS OS USUARIOS CADASTRADOS

def seleciona_usuario_por_email(cursor, email):
    comando_sql = "SELECT * FROM usuarios WHERE email = %s"
    valores = (email,)
    cursor.execute(comando_sql, valores)
    return cursor.fetchone() #RETORNA UMA TUPLA COM OS VALORES DA COLUNA DAQUELE USUARIO


def seleciona_usuario_por_id(cursor, usuario_id):
    """Retorna um usuário específico pelo ID"""
    comando_sql = "SELECT * FROM usuarios WHERE id = %s"
    valores = (usuario_id,)
    cursor.execute(comando_sql, valores)
    return cursor.fetchone()


def atualiza_usuario(cursor, conectar, novo_nome, usuario_id):
    """Atualiza o nome de um usuário pelo ID"""
    comando_sql = "UPDATE usuarios SET nome = %s WHERE id = %s"
    valores = (novo_nome, usuario_id)
    cursor.execute(comando_sql, valores)
    conectar.commit()


def deletar_usuario(cursor, conectar, usuario_id):
    """Deleta um usuário pelo ID"""
    comando_sql = "DELETE FROM usuarios WHERE id = %s"
    valores = (usuario_id,)
    cursor.execute(comando_sql, valores)
    conectar.commit()
