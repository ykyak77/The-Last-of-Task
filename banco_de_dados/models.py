from sqlalchemy import (
    create_engine, Column, Integer, String, ForeignKey, Boolean, Date, DateTime, Text, UniqueConstraint, func
) #importa funções e classes do SQLAlchemy para criação do banco e definição das colunas e tipos.

from sqlalchemy.orm import declarative_base #importa função para criar uma classe base para as classes-modelo do banco.
from sqlalchemy.orm import sessionmaker, relationship # importa para criar sessão de conexão e para definir relacionamentos entre tabelas.
from datetime import date
# Configuração do banco SQLite
engine = create_engine('sqlite:///bdprojeto.db', echo=True)
Base = declarative_base() #cria uma classe base para todos os modelos/tabelas herdarem e serem mapeados pelo SQLAlchemy.

# Definição das tabelas como classes Python
class User(Base):
    __tablename__ = 'user' #nome da tabela no banco
    user_id = Column(Integer, primary_key=True, autoincrement=True) #coluna ID, chave primária, auto-incrementada
    username = Column(String(50), unique=True, nullable=False) #coluna para nome do usuário, string, única e obrigatória
    email = Column(String(100), unique=True, nullable=False) #coluna para email, única e obrigatória
    senha = Column(String(255), nullable=False) #coluna para senha, string e obrigatória
    pilulas = Column(Integer, default=0)#coluna para pontos XP, com valor padrão zero

    # Relacionamento 1-1 com personagem
    personagem = relationship('Personagem', back_populates='user', uselist=False)
    # Relacionamento 1-N com user_tasks
    user_tasks  = relationship('UserTasks', back_populates='user')
    # Relacionamento 1-N com tasks
    tasks = relationship('Task', back_populates='user')
    # Relacionamento 1-N com inventario
    inventario = relationship('Inventario', back_populates='user')


class Personagem(Base):
    __tablename__ = 'personagem'

    personagem_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.user_id'), unique=True) #FK para usuário, única (1 personagem por usuário)
    foco = Column(Integer, default=0)
    agilidade = Column(Integer, default=0)
    inteligencia = Column(Integer, default=0)
    criatividade = Column(Integer, default=0)
    energia = Column(Integer, default=0)

    user = relationship("User", back_populates="personagem")


class Task(Base):
    __tablename__ = 'task'

    task_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.user_id'), nullable=False)
    titulo = Column(String(100), nullable=False)
    pilulas_recompensa = Column(Integer, nullable=False)
    concluido = Column(Boolean, default=False)

    user = relationship('User', back_populates='tasks')
    user_tasks = relationship('UserTasks', back_populates='task')


class UserTasks(Base):
    __tablename__ = 'user_tasks'
    __table_args__ = (UniqueConstraint('user_id', 'task_id', 'data_execucao', name='unique_task_execution'),)

    user_task_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.user_id'), nullable=False)
    task_id = Column(Integer, ForeignKey('task.task_id'), nullable=False)
    data_execucao = Column(DateTime, default=func.current_date())
    pilulas_ganhas = Column(Integer, nullable=False)

    user = relationship('User', back_populates='user_tasks')
    task = relationship('Task', back_populates='user_tasks')


class ShopItems(Base):
    __tablename__ = 'shop_items'

    item_id = Column(Integer, primary_key=True, autoincrement=True)
    item = Column(String(100), nullable=False)
    descricao = Column(Text)
    preco_pilulas = Column(Integer, nullable=False)

    inventario = relationship('Inventario', back_populates='item')


class Inventario(Base):
    __tablename__ = 'inventario'
    inventario_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.user_id'), nullable=False)
    item_id = Column(Integer, ForeignKey('shop_items.item_id'), nullable=False)
    quantidade = Column(Integer, default=1)


    user = relationship('User', back_populates='inventario')
    item = relationship('ShopItems', back_populates='inventario')


class ControleReset(Base):
    __tablename__ = 'controle_reset'
    id = Column(Integer, primary_key=True)
    data_ultima_reset = Column(Date, nullable=False, default=date.today)

if __name__ == '__main__':
    Base.metadata.create_all(engine) #cria o banco de dados
