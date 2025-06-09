from banco_de_dados.models import engine, Task, Personagem, ControleReset
from sqlalchemy.orm import sessionmaker
from datetime import datetime, date

DB_Session = sessionmaker(bind=engine)

def reiniciarTask():
    db_session = DB_Session()
    try:
        # Tenta pegar o único registro de controle (criá-lo se não existir)
        controle = db_session.query(ControleReset).first()
        if not controle:
            controle = ControleReset(data_ultima_reset=date.today())
            db_session.add(controle)
            db_session.commit()  # salva o registro inicial
            # como é a primeira vez, já pode resetar
            db_session.query(Task).update({Task.concluido: False})
            db_session.commit()
            return

        # Se já existe, compara a data
        hoje = date.today()
        if controle.data_ultima_reset != hoje:
            # reseta as tasks
            db_session.query(Task).update({Task.concluido: False})
            # atualiza a data de reset
            controle.data_ultima_reset = hoje
            db_session.commit()

    finally:
        db_session.close()

def criarTasks(id):
    tarefas = [
        Task(user_id=id, titulo="Beber agua", pilulas_recompensa=15),
        Task(user_id=id, titulo="Acordar", pilulas_recompensa=15),
        Task(user_id=id, titulo="Xingar o JUNIN", pilulas_recompensa=150)
    ]

    db_session = DB_Session()

    try:
        db_session.add_all(tarefas)
        db_session.commit()
    except Exception as e:
        db_session.rollback()
        print(f"Erro ao criar as tarefas: {e}")
    finally:
        db_session.close()


def criarPersonagem(id):
    personagem = Personagem(user_id=id)
    db_session = DB_Session()

    try:
        db_session.add(personagem)
        db_session.commit()
    except Exception as e:
        print(f"Erro ao criar o personagem {e}")
    finally:
        db_session.close()