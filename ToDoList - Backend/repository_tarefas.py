def create_tarefa(cursor, conectar, id_usuario, descricao, status="Em andamento"):
    """Insere uma nova tarefa para um usuário"""
    comando_sql = "INSERT INTO tarefas (id_usuario, descricao, status) VALUES (%s, %s, %s) RETURNING id_tarefa"
    valores = (id_usuario, descricao, status)
    cursor.execute(comando_sql, valores) #ENVIA PARA O BANCO DE DADOS. OS VALORES SERÃO INSERIDOS NA INTERFACE DA API
    conectar.commit()
    return cursor.fetchone()[0] #retorna o id gerado


def read_tarefas(cursor, id_usuario):
    """Retorna todas as tarefas de um usuário"""
    comando_sql = "SELECT * FROM tarefas WHERE id_usuario = %s ORDER BY id_tarefa"
    valores = (id_usuario,)
    cursor.execute(comando_sql, valores)
    return cursor.fetchall()


def update_tarefa(cursor, conectar, id_usuario, tarefa_id, descricao=None, status=None):
    """Atualiza descrição e/ou status de uma tarefa de um usuário"""
    if descricao is not None:
        comando_sql = "UPDATE tarefas SET descricao = %s WHERE id_tarefa = %s AND id_usuario = %s"
        valores = (descricao, tarefa_id, id_usuario)
        cursor.execute(comando_sql, valores)
    if status is not None:
        comando_sql = "UPDATE tarefas SET status = %s WHERE id_tarefa = %s AND id_usuario = %s"
        valores = (status, tarefa_id, id_usuario)
        cursor.execute(comando_sql, valores)
    conectar.commit()


def delete_tarefa(cursor, conectar, id_usuario, tarefa_id):
    """Deleta uma tarefa de um usuário"""
    comando_sql = "DELETE FROM tarefas WHERE id_tarefa = %s AND id_usuario = %s"
    valores = (tarefa_id, id_usuario)
    cursor.execute(comando_sql, valores)
    conectar.commit()


