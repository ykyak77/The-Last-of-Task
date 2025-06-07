from flask import Flask, render_template, redirect, url_for

app = Flask(__name__)

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/cadastro')
def cadastrar():
    return render_template('cadastro.html')

@app.route('/logar', methods=['GET'])
def logar():

    return redirect(url_for('menu'))

@app.route('/index')
def menu():
    return render_template('index.html')

@app.route('/perfil')
def status():
    return render_template('perfil.html')

@app.route('/loja')
def loja():
    return render_template('loja.html')

if __name__ == '__main__':
    app.run(debug=True)
