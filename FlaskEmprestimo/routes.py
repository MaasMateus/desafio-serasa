from flask import render_template, flash, url_for, request, redirect
from FlaskEmprestimo import app, db, bcrypt
from FlaskEmprestimo.models import Usuario, Emprestimo
from FlaskEmprestimo.forms import CadastrarUsuarioForm, LoginForm
from flask_login import login_user, current_user

# Definição das rotas do site, métodos e usados nelas e as páginas que devem ser retornadas
  
@app.route('/')
def index():
    """
    Carrega a página principal quando se inicia a aplicação e quando o usuário volta para ela.
    """
    return render_template('index.html')

@app.route('/cadastro', methods=['GET', 'POST'])

def cadastro():
    """
    Criando uma instância da classe usuário com os dados do cadastro, caso os campos estejam
    corretamente preenchidos, o usuário é redirecionado para a página principal e 
    sua conta é inserida no banco de dados, caso contrário, a página é recarregada
    e os erros são mostrados ao usuário.
    """
    if current_user.is_authenticated:
        return(redirect(url_for('index')))

    form = CadastrarUsuarioForm()
    
    if form.validate_on_submit():
        
        senha_hash = bcrypt.generate_password_hash(form.senha.data).decode('utf-8')
        usuario = Usuario(nome=form.nome.data, cpf=form.cpf.data, email=form.email.data,senha=senha_hash)
        db.session.add(usuario)
        db.session.commit()

        flash('Conta criada com sucesso!', 'success')
        return redirect(url_for('index'))

    return render_template('cadastro.html', title='Cadastrar', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Verifica se um usuário com o CPF informado existe no banco de dados,
    caso ele exista, se compara a senha digitada por ele com a senha em hash
    utilizada no banco de dados.

    Caso a senha não corresponda com o CPF informado, uma mensagem será mostrada
    ao usuário.

    Caso o CPF e senha sejam correspondentes, uma sessão será iniciada para este
    usuário, que pode assinalar um checkbox para se manter logado.
    """
    if current_user.is_authenticated:
        return(redirect(url_for('index')))

    form = LoginForm()
    if form.validate_on_submit():

        usuario = Usuario.query.filter_by(cpf=form.cpf.data).first()
        if usuario and bcrypt.check_password_hash(usuario.senha, form.senha.data):
            login_user(usuario, form.lembrar.data)
            return(redirect(url_for('index')))
        else:
            flash('Login mal sucedido. Verifique seu CPF e sua senha', 'danger')

    return render_template('login.html', title='Login', form=form)
