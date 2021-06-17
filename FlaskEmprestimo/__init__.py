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

# Import após a inicialização do programa pois alguns módulos importados requerem
# variáveis inicializadas acima
from FlaskEmprestimo import routes