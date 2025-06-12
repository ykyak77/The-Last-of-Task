from banco_de_dados.models import engine, Task, Personagem, ControleReset, ShopItens
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

def criarTasks(id, dados):
    tarefas = [
        Task(user_id=id, titulo="Evite telas 1h antes de dormir", pilulas_recompensa=30),
        Task(user_id=id, titulo="Dormir e acordar sempre no mesmo horário", pilulas_recompensa=15),
        Task(user_id=id, titulo="7 a 8 horas de sonho", pilulas_recompensa=35),
        Task(user_id=id, titulo="Evitar picos de açúcar", pilulas_recompensa=45),
        Task(user_id=id, titulo="Tomar 2 litros de água por dia", pilulas_recompensa=50),
        Task(user_id=id, titulo="Separar 5 minutos por dia para respirar fundo e relaxar", pilulas_recompensa=10),
        Task(user_id=id, titulo="Aplicar técnica Pomodoro: 25 min de foco + 5 min de pausa", pilulas_recompensa=15)
    ]

    rotina = []

    # Rotina matinal
    rotina.append(Task(user_id=id, titulo=f"Acordar às {dados['acorda']}h e beber um copo de água", pilulas_recompensa=25))
    rotina.append(Task(user_id=id, titulo="Fazer um café da manhã equilibrado (proteínas + carboidratos)", pilulas_recompensa=15))
    rotina.append(Task(user_id=id, titulo='Comece o dia com intenção: "Qual é minha prioridade hoje?"', pilulas_recompensa=5))

    # Exercício (espera bool)
    if dados["exercicio"]:
        rotina.append(Task(user_id=id, titulo="Fazer exercícios físicos, 30 minutos por sessão", pilulas_recompensa=45))
    else:
        rotina.append(Task(user_id=id, titulo="Caminhada leve 20 minutos", pilulas_recompensa=45))

    # Objetivos são uma lista, vamos iterar
    if "reduzir estresse" in dados["objetivo"]:
        rotina.append(Task(user_id=id, titulo="Praticar 5 minutos de respiração consciente ou meditação por dia", pilulas_recompensa=15))
        rotina.append(Task(user_id=id, titulo="Fazer pausas regulares durante o trabalho/estudo para relaxar", pilulas_recompensa=15))

    if "melhorar sono" in dados["objetivo"]:
        rotina.append(Task(user_id=id, titulo=f"Ir para a cama até às {dados['dorme']}h", pilulas_recompensa=10))
        rotina.append(Task(user_id=id, titulo="Evitar telas pelo menos 1 hora antes de dormir", pilulas_recompensa=50))

    if "ter mais energia" in dados["objetivo"]:
        rotina.append(Task(user_id=id, titulo="Manter alimentação balanceada", pilulas_recompensa=40))
        rotina.append(Task(user_id=id, titulo="Incluir pequenas pausas para alongamento durante o dia", pilulas_recompensa=25))

    if "parar de procrastinar" in dados["objetivo"]:
        rotina.append(Task(user_id=id, titulo="Definir 3 tarefas prioritárias para o dia", pilulas_recompensa=25))

    db_session = DB_Session()

    try:
        db_session.add_all(rotina)
        db_session.add_all(tarefas)
        db_session.commit()
        return True
    except Exception as e:
        db_session.rollback()
        print(f"Erro ao criar as tarefas: {e}")
        return False
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


def criarItens():
    db_session = DB_Session()

    if db_session.query(ShopItens).first():
        db_session.close()
        return  # Já existem itens, então não insere de novo

    itens = [
        ShopItens(item="longinus", nome="Lança de Longinus", descricao="Arma divina capaz de perfurar qualquer barreira, inclusive almas.", preco_pilulas=300),
        ShopItens(item="triforce", nome="Triforce", descricao="Artefato sagrado que concede desejos e poder.", preco_pilulas=200),
        ShopItens(item="excalibur", nome="Excalibur", descricao="Espada lendária empunhada apenas pelo verdadeiro rei.", preco_pilulas=150),
        ShopItens(item="ocarina", nome="Ocarina do Tempo", descricao="Instrumento mágico que controla o tempo.", preco_pilulas=100),
        ShopItens(item="master_sword", nome="Master Sword", descricao="A lendária lâmina capaz de selar o mal.", preco_pilulas=75),
        ShopItens(item="kunai", nome="Kunai Explosiva", descricao="Arma ninja com selo explosivo.", preco_pilulas=45),
        ShopItens(item="nevoa", nome="Faca da Névoa", descricao="Arma silenciosa que confunde e cega inimigos.", preco_pilulas=70),
        ShopItens(item="samehada", nome="Samehada", descricao="Lâmina viva que absorve chakra.", preco_pilulas=125),
        ShopItens(item="estus", nome="Estus Flask", descricao="Cura gradualmente a vida, essencial em combates longos.", preco_pilulas=100),
        ShopItens(item="red", nome="Poção Vermelha", descricao="Poção de cura gradual", preco_pilulas=25),
        ShopItens(item="molotov", nome="Coquetel Molotov", descricao="Arma improvisada feita com garrafa, pano e álcool. Causa dano em área.", preco_pilulas=15)
    ]

    try:
        db_session.add_all(itens)
        db_session.commit()
    except Exception as e:
        print(e)
    finally:
        db_session.close()
