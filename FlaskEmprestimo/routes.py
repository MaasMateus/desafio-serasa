from flask import render_template, flash, url_for, request, redirect
from FlaskEmprestimo import app, db, bcrypt
from FlaskEmprestimo.models import Usuario, Emprestimo
from FlaskEmprestimo.forms import CadastrarUsuarioForm, LoginForm, PedirEmprestimoForm
from flask_login import login_user, logout_user, current_user, login_required

# Definição das rotas do site, métodos e usados nelas e as páginas que devem ser retornadas
  
@app.route('/')
def index():
    """
    Carrega a página principal quando se inicia a aplicação e quando o usuário volta para ela.
    Se o usuário não está logado, ele será redirecionado para a página de requisição de empréstimos. 
    """
    if current_user.is_authenticated:
        return render_template('index.html')
    else:
        return redirect(url_for('emprestimo'))

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

    Caso o usuário tente fazer uma ação que requer estar logado numa conta, ele pode
    realizar o login e então será redirecionado para a página que tentou acessar anteriormente 
    """
    if current_user.is_authenticated:
        return(redirect(url_for('index')))

    form = LoginForm()
    if form.validate_on_submit():

        usuario = Usuario.query.filter_by(cpf=form.cpf.data).first()
        if usuario and bcrypt.check_password_hash(usuario.senha, form.senha.data):
            login_user(usuario, form.lembrar.data)
            proxima_pag = request.args.get('next')

            return redirect(proxima_pag) if proxima_pag else redirect(url_for('index'))
        else:
            flash('Login mal sucedido. Verifique seu CPF e sua senha', 'danger')

    return render_template('login.html', title='Login', form=form)

@app.route('/logout')
def logout():
    """
    Apenas disponível quando um usuário já está logado, apenas desloga a conta e atualiza a páginia.
    """
    logout_user()
    return redirect(url_for('index'))

@app.route('/perfil')
@login_required
def perfil():
    """
    Apenas disponível quando um usuário estiver logado, exibe as informações do perfil do usuário
    """
    qtd_emprestimos = 0
    emprestimos = Usuario.query.filter_by(id=current_user.id).first().emprestimos
    for emprestimo in emprestimos:
        if emprestimo.ativo:
            qtd_emprestimos += 1 
    return render_template('perfil.html', title='Perfil', qtd_emprestimos=qtd_emprestimos)

@app.route('/perfil/detalhes_emprestimos')
@login_required
def detalhes_perfil():
    """
    Apenas disponível quando um usuário estiver logado, mostra o histórico de empréstimos do
    usuário e quais deles ainda estão ativos
    """
    emprestimos = Emprestimo.query.filter_by(beneficiado=current_user).order_by(Emprestimo.ativo)
    return render_template('detalhes_emprestimos.html',title='Detalhes', emprestimos=emprestimos)

@app.route('/emprestimo')
def emprestimo():
    """
    Responsável por renderizar os campos que devem ser preenchidos por um usuário para que
    ele possa pedir um empréstimo. O empréstimo pode apenas ser concluído se o usuário estiver logado.
    É a página para a qual um usuário é redirecionado caso não esteja logado.
    """
    form = PedirEmprestimoForm()
    return render_template('emprestimo.html', title='Emprestimo', form=form)

@app.route('/emprestimo/confirmar_emprestimo')
@login_required
def confirmar_emprestimo():
    pass
    