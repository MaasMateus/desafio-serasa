from enum import unique
from FlaskEmprestimo import db, login_manager
from flask_login import UserMixin

# Criação das classes que darão origem às tabelas do banco de dados local

# Método __repr__() define o que uma instância dessa classe deve retornar
# caso seja transformada em uma string
@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))


class Usuario(db.Model, UserMixin):
    """
    Classe usada para representar um usuário no banco de dados,
    cada atributo da classe representando uma coluna na tabela usuario.
    Utilizada no cadastro (quando criando um novo usuário e na verificação
    de usuário já existente) e no login (para varificar se os dados inseridos
    pelo usuário correspondem à uma conta no banco de dados).
    Herda atributos de uma classe padrão para modelos de banco de dados e uma
    classe padrão para usuários.

    Atributos:
        id: Valor atribuído automáticamente para uma instancia da classe
        quando ela for inserida no banco de dados

        nome: Nome informado pelo usuário

        cpf: Número de cpf informado pelo usuário

        email: Endereço de e-mail informado pelo usuário 

        senha: Hash da senha informada pelo usuário

        salario: Salário informado pelo usuário enquanto se preenche
        o formulário de requisição para um empréstimo

        emprestimos: Relação de empréstimos já realizados pelo usuário, ativos ou não

    """
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    cpf = db.Column(db.String(11), nullable = False, unique=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    senha = db.Column(db.String(60), nullable=False)
    salario = db.Column(db.Integer)
    emprestimos = db.relationship('Emprestimo', backref='beneficiado', lazy=True)

    def __repr__(self):
        return f"Usuário: ('{self.nome}', '{self.cpf}')"


class Emprestimo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    valor = db.Column(db.Integer, nullable=False)
    parcelas = db.Column(db.Integer, nullable=False)
    parcelas_restantes = db.Column(db.Integer, nullable=False)
    valor_parcela = db.Column(db.Integer, nullable=False)
    ativo = db.Column(db.Boolean)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)

    def __repr__(self):
        return f"""Valor: R$ {self.valor}
Parcelas restantes: {self.parcelas_restantes}
Valor à ser pago: {self.valor_parcela * self.parcelas_restantes}"""