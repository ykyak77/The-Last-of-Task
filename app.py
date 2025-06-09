from flask import Flask, render_template, redirect, url_for, flash, request, session
from sqlalchemy.sql.visitors import replacement_traverse
from werkzeug.security import generate_password_hash, check_password_hash
from banco_de_dados.models import engine, Base, User, Task
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from functools import wraps
from banco_de_dados.services import criarTasks, criarPersonagem, reiniciarTask


app = Flask(__name__)
app.secret_key = "the_last_of_task"

#configurando sessao do SqlAlchemy
DB_Session = sessionmaker(bind=engine)
Base.metadata.create_all(engine) # criar tabelas se não existirem

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
            criarTasks(newUser.user_id)
            criarPersonagem(newUser.user_id)
            return redirect(url_for('menu'))
        except IntegrityError:
            db_session.rollback()
            flash('Nome do Usuario ou email ja existe')
            return render_template(url_for('cadastrar'))
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
        else:
            flash("Erro! Email ou senha incorretos")
            return render_template('login.html', email=email)

    return redirect(url_for('menu'))

@app.route('/index')
@login_required
def menu():
    reiniciarTask()

    db_session = DB_Session()
    try:
        tasks = db_session.query(Task).all()
        # tasks = db_session.query(Task).filter(Task.concluido.is_(True)).all() #exibe somente se a tarefa nao foi executada
    finally:
        db_session.close()

    return render_template('index.html', tarefas=tasks)

@app.route('/concluir_tarefa/<int:task_id>', methods=['POST'])
@login_required
def concluirTarefa(task_id):
    db_session = DB_Session()
    try:
        tarefa = db_session.query(Task).get(task_id)
        if tarefa and tarefa.user.user_id == session['user_id']:
            tarefa.concluido = True
            db_session.commit()
    finally:
        db_session.close()

    return redirect(url_for('menu'))

@app.route('/perfil')
@login_required
def status():
    return render_template('perfil.html')

@app.route('/loja')
@login_required
def loja():
    return render_template('loja.html')

if __name__ == '__main__':
    app.run(debug=True)
