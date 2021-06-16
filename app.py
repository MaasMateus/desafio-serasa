from flask import Flask, render_template, flash, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
import forms

# Inicialização da aplicação
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///teste.db'
app.config['SECRET_KEY'] = '35d9a306792f2de5075a4f32bfe09da6'
db = SQLAlchemy(app)

# Definição das rotas, métodos usados nelas e as páginas que devem ser retornadas 
@app.route('/')
def index():
    return render_template('home.html')

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    form = forms.CadastrarUsuarioForm()
    if form.validate_on_submit():
        flash('Conta criada com sucesso!', 'success')
        # ^ Cria um alerta para o usuário
        return redirect(url_for('index'))
    return render_template('cadastro.html', title='Cadastrar', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = forms.LoginForm()
    return render_template('login.html', title='Login', form=form)


if __name__ == "__main__" :
    app.run(debug=True)