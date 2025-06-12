

# 🎮 The Last of Task

**The Last of Task** é um sistema **gamificado** de tarefas que transforma atividades rotineiras em uma jornada divertida. Ao completar tarefas, você ganha **MOEDAS** e com elas, você pode evolui seu personagem e adquirir itens para colecionar. Uma forma inovadora de unir **produtividade com motivação**!

---

## 🧩 Funcionalidades

- Cadastro e login de usuários
- Registro, visualização e conclusão de tarefas
- Sistema de recompensa
- Personagem com atributos customizáveis
- Loja para compra de itens
- Interface simples, responsiva e intuitiva

---

## 🛠️ Tecnologias Utilizadas

- **Python 3.x**
- **Flask** — framework web
- **SQLAlchemy** — ORM para banco de dados
- **SQLite** — banco de dados leve e local
- **Jinja2** — motor de templates HTML
- **HTML/CSS** — estilização e estrutura

---

## 🏗️ Estrutura do Projeto

```
The-Last-of-Task/
├── banco_de_dados/
│   ├── models.py
│   └── services.py
├── static/
│   ├── imagens/
│   │   ├── imgItens/
│   │   └──  status/
│   └── style.css
├── templates/
│   ├── cadastro.html
│   ├── index.html
│   ├── inventario.html
│   ├── login.html
│   ├── loja.html
│   ├── perfil.html
│   └── questionario.html
├── app.py
└── teste.py
```

---
## 🚀 Como Executar o Projeto

1. Clone o repositório:

```
git clone https://github.com/ykyak77/The-Last-of-Task.git
cd The-Last-of-Task
```

2. Crie e ative um ambiente virtual:

```
python -m venv venv
source venv/bin/activate     # Linux/macOS
venv\Scripts\activate      # Windows
```

3. Instale as dependências:

```
pip install -r requirements.txt
```

> Caso não tenha o `requirements.txt`, use:
```
pip install flask sqlalchemy
```

4. Inicie o servidor Flask:

```
python app.py
```

5. Acesse via navegador:

```
http://127.0.0.1:5000/
```

---


## 🧠 Aprendizados

- Flask com GET e POST
- Autenticação com Flask-Login
- ORM com SQLAlchemy
- Templates dinâmicos
- Lógica de gamificação


---

[ 🛰 Canva](https://www.canva.com/design/DAGp-nEM3Yk/1ATj6sgAM-DGTePecGqV4g/edit?utm_content=DAGp-nEM3Yk&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton)
