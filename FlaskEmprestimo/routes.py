from flask import render_template, flash, url_for, request, redirect, abort
from FlaskEmprestimo import app, db, bcrypt, is_number, ofertas
from FlaskEmprestimo.models import Usuario, Emprestimo
from FlaskEmprestimo.forms import CadastrarUsuarioForm, LoginForm, PedirEmprestimoForm, ConfirmarEmprestimoForm
from flask_login import login_user, logout_user, current_user, login_required

# Definição das rotas do site, métodos e usados nelas e as páginas que devem ser retornadas
  
@app.route('/', methods=['GET', 'POST'])
def index():
    """
    Carrega a página principal quando se inicia a aplicação e quando o usuário volta para ela.
    Se o usuário não está logado, ele será redirecionado para a página de requisição de empréstimos. 
    """
    if current_user.is_authenticated:

        lista_ofertas = ofertas(current_user)

        return render_template('index.html', ofertas=lista_ofertas)
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
        usuario = Usuario(nome=form.nome.data, cpf=form.cpf.data, email=form.email.data,
            senha=senha_hash, salario=form.salario.data)
        db.session.add(usuario)
        db.session.commit()
        login_user(usuario, form.lembrar.data)

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

@app.route('/perfil/emprestimos')
@login_required
def detalhes_emprestimos():
    """
    Apenas disponível quando um usuário estiver logado, mostra o histórico de empréstimos do
    usuário e quais deles ainda estão ativos
    """
    emprestimos = Emprestimo.query.filter_by(beneficiado=current_user).order_by(Emprestimo.parcelas_restantes)

    return render_template('detalhes_emprestimos.html',title='Detalhes', emprestimos=emprestimos)

@app.route('/emprestimo', methods=['GET', 'POST'])
def emprestimo():
    """
    Responsável por renderizar os campos que devem ser preenchidos por um usuário para que
    ele possa pedir um empréstimo. O empréstimo pode apenas ser concluído se o usuário estiver logado.
    É a página para a qual um usuário é redirecionado caso não esteja logado.
    """
    form = PedirEmprestimoForm()

    return render_template('emprestimo.html', title='Emprestimo', form=form)

@app.route('/emprestimo/confirmar', methods=['GET', 'POST'])
def confirmar_emprestimo():
    """
    Tela para revisão do empréstimo, onde são mostradas informações mais detalhadas sobre o empréstimo
    que o usuário deseja, verifica se o valor do empréstimo está dentro dos limites oferecidos e retorna
    mensagens de erro caso não seja.
    Checa se o usuário está logado através de if, ao invés de com @login_required por conta de erros na 
    hora de redirecionar o usuário de volta para a página, por conta da falta de valores nos formulários que são
    pedidos na rota /emprestimo.
    A função is_number() é utilizada para garantir que nenhum valor que não possa ser convertido para um valor
    numérico possa ser atribuído tanto para o valor do empréstimo quanto para o salário do usuário.
    O usuário pode chegar à essa rota através da rota /emprestimo ou clicando em uma oferta na página inicial,
    as ofertas passam valores por URL e a rota /emprestimo passa os valores por formulário.
    """
    
    if not current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ConfirmarEmprestimoForm()

    valor = request.values.get('valor')
    if is_number(valor):

        salario = request.values.get('salario')
        if is_number(salario):

            valor = round(float(request.values.get('valor')), 2)
            parcelas = int(request.values.get('parcelas'))
            salario = float(request.values.get('salario'))
            valor_a_pagar = round(float(valor) * 1.15, 2)
            data = {
                'valor': valor,
                'parcelas': parcelas,
                'salario': salario,
                'valor_a_pagar': valor_a_pagar,
                'valor_parcela': round(valor_a_pagar / parcelas, 2),
            }
            if valor > 50000:
                flash('Valor muito alto, o empréstimo deve ser menor que R$ 50000.00','danger')
                return redirect(url_for('emprestimo'))

            elif valor < 1000:
                flash('Valor muito baixo, o empréstimo deve ser maior que R$ 1000.00','danger')
                return redirect(url_for('emprestimo'))
            
            salario_ativo = Usuario.query.filter_by(id=current_user.id)
            if salario_ativo != salario:
                current_user.salario = salario
                db.session.commit()
                flash('Sua renda foi atualizada',' success')

            return render_template('confirmar_emprestimo.html', form=form, data=data)
    
        else:
            flash('Valor de salário invalido','danger')
        return redirect(url_for('emprestimo'))
    else:
        flash('Valor para empréstimo invalido','danger')
        return redirect(url_for('emprestimo'))

@app.route('/emprestimo/confirmar/upload', methods=['GET', 'POST'])
@login_required
def upload_emprestimo():
    if request.method == 'POST':
        if request.form['submit_btn'] == 'Cancelar':
            flash('Empréstimo cancelado','danger')
            return redirect(url_for('emprestimo'))
        elif request.form['submit_btn'] == 'Confirmar':
            r = request.form

            emprestimo = Emprestimo(valor=float(r['valor_a_pagar']), parcelas=int(r['parcelas']), valor_parcela=float(r['valor_parcela']),
                    parcelas_restantes=int(r['parcelas']), ativo=True, id_usuario=current_user.id)

            db.session.add(emprestimo)
            db.session.commit()

            if emprestimo.valor_parcela > float(r['salario']) / 10 * 3:
                flash('Sua requisição foi enviada para analize', 'danger')

            return redirect(url_for('detalhes_emprestimos'))
        else:
            pass # unknown
    return redirect(url_for('emprestimo'))

@app.route('/perfil/emprestimos/pagar/<int:emprestimo_id>', methods=['GET', 'POST'])
@login_required
def pagar_emprestimo(emprestimo_id):
    emprestimo = Emprestimo.query.get_or_404(emprestimo_id)
    if emprestimo.beneficiado != current_user:
        abort(403)
    else:
        emprestimo.parcelas_restantes -= 1
        if emprestimo.parcelas_restantes == 0:
            emprestimo.ativo = False

        db.session.commit()
        flash('Parcela do empréstimo paga!', 'success')
        return redirect(url_for('detalhes_emprestimos'))