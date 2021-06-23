from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

# Inicialização da aplicação
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///teste.db'
app.config['SECRET_KEY'] = '35d9a306792f2de5075a4f32bfe09da6'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Você precisa estar logado para acessar essa página'
login_manager.login_message_category = 'info'

def is_number(n):
    try:
        float(n)
        return True
    except ValueError:
        return False

# Função para checar se um valor é ou não um número

def ofertas(usuario):
    parcela_max = usuario.salario / 10 * 3
    ofertas = []
    if parcela_max > 1600:
        valor = 50000
        parcelas = 36
        oferta = {
            'titulo': 'Está querendo trocar de carro?',
            'valor': valor,
            'parcelas': parcelas,

        }
        ofertas.append(oferta)
    # if parcela_max

    return ofertas

# Retorna para o usuário 3 ofertas, dependendo de sua renda mensal


# Import após a inicialização do programa pois alguns módulos importados requerem
# variáveis inicializadas acima
from FlaskEmprestimo import routes