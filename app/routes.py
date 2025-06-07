def cadastrar_usuario(username, email, senha):
    conexao, cursor = conectar()
    if not conexao or not cursor:
        return False, "Erro na conexão"

    try:
        cursor.execute("INSERT INTO user (username, email, senha) VALUES (?, ?, ?)", (username, email, senha))
        conexao.commit()
        return True, "Usuário cadastrado com sucesso"
    except sqlite3.IntegrityError as e:
        if 'UNIQUE constraint failed: user.username' in str(e):
            return False, "Username já existe"
        elif 'UNIQUE constraint failed: user.email' in str(e):
            return False, "Email já existe"
        else:
            return False, f"Erro de integridade: {e}"
    except sqlite3.Error as e:
        return False, f"Erro ao cadastrar: {e}"
    finally:
        conexao.close()


def login_usuario(username, senha):
    conexao, cursor = conectar()
    if not conexao or not cursor:
        return False, "Erro na conexão"

    try:
        cursor.execute("SELECT senha FROM user WHERE username = ?", (username,))
        result = cursor.fetchone()
        if result is None:
            return False, "Usuário não encontrado"
        senha_banco = result[0]
        if senha == senha_banco:
            return True, "Login realizado com sucesso"
        else:
            return False, "Senha incorreta"
    except sqlite3.Error as e:
        return False, f"Erro ao realizar login: {e}"
    finally:
        conexao.close()


def criar_task(titulo, xp_recompensa, recorrencia='uma', ativo=1):
    conexao, cursor = conectar()
    if not conexao or not cursor:
        return False, "Erro na conexão"

    try:
        cursor.execute("""
            INSERT INTO task (titulo, xp_recompensa, recorrencia, ativo) 
            VALUES (?, ?, ?, ?)
        """, (titulo, xp_recompensa, recorrencia, ativo))
        conexao.commit()
        return True, "Tarefa criada com sucesso"
    except sqlite3.Error as e:
        return False, f"Erro ao criar tarefa: {e}"
    finally:
        conexao.close()


def listar_tasks_usuario(user_id):
    conexao, cursor = conectar()
    if not conexao or not cursor:
        return None

    try:
        cursor.execute("""
            SELECT t.task_id, t.titulo, t.xp_recompensa, t.recorrencia, t.ativo 
            FROM task t
            JOIN user_tasks ut ON t.task_id = ut.task_id
            WHERE ut.user_id = ?
        """, (user_id,))
        resultados = cursor.fetchall()
        return resultados
    except sqlite3.Error as e:
        print(f"Erro ao listar tarefas: {e}")
        return None
    finally:
        conexao.close()