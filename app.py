from flask import Flask, render_template, redirect, url_for, flash, request, session
from sqlalchemy.sql.visitors import replacement_traverse
from datetime import datetime

from sqlalchemy.testing.suite.test_reflection import users
from werkzeug.security import generate_password_hash, check_password_hash
from banco_de_dados.models import engine, Base, User, Task, UserTasks, ShopItens, Inventario
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from functools import wraps
from banco_de_dados.services import criarTasks, criarPersonagem, reiniciarTask, criarItens


app = Flask(__name__)
app.secret_key = "the_last_of_task"

#configurando sessao do SqlAlchemy
DB_Session = sessionmaker(bind=engine)

def iniciar_banco():
    Base.metadata.create_all(engine) # criar tabelas se não existirem
    criarItens()


# Decorador para proteger rotas
def login_required(f): #recebe outra funcao como parametro, por exemplo a rota index
    @wraps(f) #mantem o nome e a documentação da função original
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash("Você precisa estar logado.")
            return redirect(url_for('login')) # se nao tiver logado, irar impedir o acesso do usario a aqla pagina
        return f(*args, **kwargs) #se logado, execulta a funcao normalmente
    return decorated_function

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/cadastro', methods=['GET','POST'])
def cadastrar():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        senha = request.form.get('senha')
        senhaConfir = request.form.get('senhaConfirma')

        if not username or not email or not senha:
            flash('Campo vazio, por favor preencha-o')
            return render_template('cadastro.html', username=username, email=email)

        if senha != senhaConfir:
            flash('Senhas não coincidem! Tente novamente')
            return render_template('cadastro.html', username=username, email=email)

        senhaHash = generate_password_hash(senha)

        db_session = DB_Session()

        newUser = User(username=username, email=email, senha=senhaHash)

        try:
            db_session.add(newUser)
            db_session.commit()
            session['user_id'] = newUser.user_id
            criarPersonagem(newUser.user_id)
            return redirect(url_for('coletarDados'))
        except IntegrityError:
            db_session.rollback()
            flash('Nome do Usuario ou email ja existe')
            return render_template('cadastro.html', username=username, email=email)
        finally:
            db_session.close()

    return render_template('cadastro.html')

@app.route('/logar', methods=['POST'])
def logar():
    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')

        if not email or not senha:
            flash("Preencha usuário e senha!")
            return render_template('login.html', email=email)

        db_session = DB_Session()

        user = db_session.query(User).filter_by(email=email).first()
        db_session.close()

        if user and check_password_hash(user.senha, senha):
            session['user_id'] = user.user_id
            return redirect(url_for('menu'))
        elif not user:
            flash("Usuario não existe")
            return render_template('login.html', email=email)
        else:
            flash("Erro! Email ou senha incorretos")
            return render_template('login.html', email=email)

    return redirect(url_for('menu'))

@app.route('/menu')
@login_required
def menu():
    reiniciarTask()

    db_session = DB_Session()
    try:
        user_id = session['user_id']
        user = db_session.query(User).get(user_id)
        pilulas = user.pilulas if user else 0

        tasks = db_session.query(Task).filter(Task.user_id.is_(user_id)).all()
        # tasks = db_session.query(Task).filter(Task.concluido.is_(True)).all() #exibe somente se a tarefa nao foi executada
    finally:
        db_session.close()

    return render_template('index.html', tarefas=tasks, pilulas_totais=pilulas)


@app.route('/concluir_tarefa/<int:task_id>', methods=['POST'])
@login_required
def concluirTarefa(task_id):
    db_session = DB_Session()
    try:
        tarefa = db_session.query(Task).get(task_id)
        user_id = session['user_id']

        if tarefa and tarefa.user.user_id == user_id:
            tarefa.concluido = True

            pilulas = getattr(tarefa, 'pilulas_recompensa', 0)
            data = datetime.now()
            registro = UserTasks(user_id=user_id, task_id=task_id, data_execucao=data, pilulas_ganhas=pilulas)
            db_session.add(registro)

            #somar e atribuir ao total de pilulas do usuario
            user = db_session.query(User).get(user_id)
            user.pilulas += pilulas

            db_session.commit()
    except Exception as e:
        db_session.rollback()
        print(f"Erro ao realizar tarefas: {e}")
    finally:
        db_session.close()

    return redirect(url_for('menu'))


@app.route('/questionario', methods=['GET','POST'])
@login_required
def coletarDados():
    if request.method == 'POST':
        user_id = session.get('user_id')
        # Pega os dados do formulário
        idade = request.form.get('idade')
        acorda = request.form.get('acorda')
        dorme = request.form.get('dorme')
        objetivos = request.form.getlist('objetivo')
        exercicio = request.form.get('exercicio')

        # Converter os dados para os tipos corretos
        dados = {
            "idade": int(idade) if idade else 0,
            "acorda": int(acorda) if acorda else 0,
            "dorme": int(dorme) if dorme else 0,
            "objetivo": objetivos,  # lista de strings
            "exercicio": True if exercicio == "sim" else False,
        }

        if criarTasks(user_id, dados):
            return redirect(url_for('menu'))
        else:
            flash('Algum erro ocorreu, por favor tente novamente')
            return render_template('questionario.html')

    return render_template('questionario.html')



@app.route('/perfil')
@login_required
def status():
    return render_template('perfil.html')

@app.route('/loja')
@login_required
def loja():
    db_session = DB_Session()
    user_id = session['user_id']
    try:
        itensComprados = db_session.query(Inventario.item_id).filter_by(user_id=user_id)
        itens = db_session.query(ShopItens).filter(~ShopItens.item_id.in_(itensComprados)).all()
        user = db_session.query(User).get(user_id)
    except:
        flash("Erro ao encontar itens na loja")
        return render_template('loja.html')
    finally:
        db_session.close()

    return render_template('loja.html', itens=itens, user=user)


@app.route('/comprar_item/<int:item_id>', methods=['POST'])
@login_required
def comprarItem(item_id):
    db_session = DB_Session()
    try:
        user_id = session['user_id']
        item = db_session.query(ShopItens).get(item_id)
        user = db_session.query(User).get(user_id)

        if user.pilulas < item.preco_pilulas:
            return "Saldo insuficiente"  # ou redirecionar com flash

        if item:
            inventerio = Inventario(user_id=user_id,item_id=item_id, comprado=True)
            db_session.add(inventerio)

            user.pilulas -= item.preco_pilulas

            db_session.commit()
    except Exception as e:
        db_session.rollback()
        print(f"Erro ao realizar tarefas: {e}")
    finally:
        db_session.close()
    return redirect(url_for('loja'))  # ou render_template


@app.route('/inventario')
@login_required
def inventario():
    db_session = DB_Session()
    user_id = session['user_id']

    try:
        itensComprados = db_session.query(Inventario.item_id).filter_by(user_id=user_id)
        itens = db_session.query(ShopItens).filter(ShopItens.item_id.in_(itensComprados)).all()
    except Exception as e:
        flash("Erro ao encontar itens na loja")
        return render_template('inventario.html')
    finally:
        db_session.close()

    return render_template('inventario.html', itens=itens)


if __name__ == '__main__':
    iniciar_banco()
    app.run(debug=True)
