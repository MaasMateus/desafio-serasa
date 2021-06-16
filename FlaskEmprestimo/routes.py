from flask import render_template, flash, url_for, request, redirect
from FlaskEmprestimo import app
from FlaskEmprestimo.models import Usuario, Emprestimo
from FlaskEmprestimo.forms import CadastrarUsuarioForm, LoginForm

# Definição das rotas do site, métodos usados nelas e as páginas que devem ser retornadas 
@app.route('/')
def index():
    return render_template('home.html')

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    form = CadastrarUsuarioForm()
    if form.validate_on_submit():
        flash('Conta criada com sucesso!', 'success')
        # ^ Cria um alerta para o usuário
        return redirect(url_for('index'))
    return render_template('cadastro.html', title='Cadastrar', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    return render_template('login.html', title='Login', form=form)
