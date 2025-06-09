from banco_de_dados.models import engine, Task, User, UserTasks, ShopItems, Personagem
from sqlalchemy.orm import sessionmaker

DB_Session = sessionmaker(bind=engine)

def select(model):
    db_session = DB_Session()
    try:
        registros = db_session.query(model).all()
        if registros:
            print(f"--- Dados da tabela {model.__tablename__} ---")
            for registro in registros:
                print(registro.__dict__)
        else:
            print(f"Nenhum registro encontrado na tabela {model.__tablename__}.")
    except Exception as e:
        print(f"Erro ao buscar dados da tabela: {e}")
    finally:
        db_session.close()


if __name__ == '__main__':
    select(Task)