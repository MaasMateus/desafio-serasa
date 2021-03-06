from decimal import Decimal
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, PasswordField, DecimalField, IntegerField
from wtforms.fields.core import SelectField
from wtforms.validators import DataRequired, Length, EqualTo, Email, NumberRange, ValidationError
from FlaskEmprestimo.models import Usuario

class CadastrarUsuarioForm(FlaskForm):
    """
    Classe responsável por represntar os campos de preenchimento durante o cadastro.
    Usada para criar uma instância de usuário no banco de dados

    Atributos:
        Todos os atributos com "campo" em sua descrição devem ser preenchidos pelo usuário.
        Todos os campos devem ser obrigatóriamente preenchidos para que uma conta possa ser criada. 

        nome: Campo de texto para o nome

        cpf: Campo de texto para o número de cpf

        email: Campo de texto para o endereço de e-mail 

        senha: Campo para a senha

        confirmar_senha: Segundo campo para a senha, utilizado para confirmar a 
        primeira senha, caso estejam diferentes, o usuário terá que informar ambas novamente

        salario: Campo para o valor do salário do usuário 

        lembrar: Checkbox que, se assinalada pelo usuário ao criar sua conta, vai lembrar de 
        sua conta ao entrar novamente

        submit: Botão que deve ser apertado pelo usuário após o preenchimento de todos os dados
        anteriores, é usado para ativar a verificação dos dados e, se estiverem corretos, inserir
        os dados no banco de dados

    Métodos:
        Métodos com validate_[atributo do form] são chamados automaticamente pelo
        Flask quando se tenta enviar os dados que foram preenchidos no campo referente
        ao atributo de mesmo nome

        validate_cpf(): Verifica se o mesmo número de CPF já foi utilizado por outro usuário,
        não verifica se o número de CPF em si é válido

        validate_email(): Verifica se o mesmo e-mail já foi utilzado por outro usuário 
    """


    nome = StringField('Nome Completo', validators=[DataRequired(), Length(min=2, max=50)])
    
    cpf = StringField('CPF (somente números)', 
        validators=[DataRequired(message='O preenchimento deste campo é obrigatório'),
        Length(min=11, max=11, message='Este campo deve conter 11 caracteres')])

    email = StringField('E-mail', 
        validators=[DataRequired(message='O preenchimento deste campo é obrigatório'),
        Email(message='Endereço de e-mail inválido')])

    senha = PasswordField('Senha', 
        validators=[DataRequired(message='O preenchimento deste campo é obrigatório')])

    confirmar_senha = PasswordField('Confirmar Senha', 
        validators=[DataRequired(message='O preenchimento deste campo é obrigatório'), 
        EqualTo('senha', message='As senhas devem ser iguais')])

    salario = DecimalField('Sua renda mensal', validators=[DataRequired(message='O preenchimento deste campo é obrigatório')])

    lembrar = BooleanField('Lembrar usuário')

    submit = SubmitField('Cadastrar')

    def validate_cpf(self, cpf):
        controle = Usuario.query.filter_by(cpf=cpf.data).first()
        if controle:
            raise ValidationError('CPF já cadastrado.')

    def validate_email(self, email):
        controle = Usuario.query.filter_by(email=email.data).first()
        if controle:
            raise ValidationError('E-mail já cadastrado.')


class LoginForm(FlaskForm):
    """
    Classe responsável por represntar os campos de preenchimento durante o login.
    Usada para verificar se os dados informados pelo usuário correspondem a uma conta existente.

    Atributos:
        Todos os atributos com "campo" em sua descrição devem ser preenchidos pelo usuário.
        Todos os campos devem ser obrigatóriamente preenchidos para que possa se entrar numa conta. 

        cpf: Campo de texto para o número de cpf

        senha: Campo para a senha

        lembrar: Checkmark que, se assinalada pelo usuário, sinaliza que o usuário não
        precisa iniciar outra sessão ao entrar no site novamente

        submit: Botão que deve ser apertado pelo usuário após o preenchimento de todos os dados
        anteriores, é usado para ativar a verificação dos dados e, se estiverem corretos, iniciar
        uma sessão para o usuário em questão
    """

    cpf = StringField('CPF (somente números)',
        validators=[DataRequired(message='O preenchimento deste campo é obrigatório'),
        Length(min=11, max=11, message='Este campo deve conter 11 caracteres')])

    senha = PasswordField('Senha',
        validators=[DataRequired(message='O preenchimento deste campo é obrigatório')])

    lembrar = BooleanField('Lembrar usuário')

    submit = SubmitField('Entrar')


class PedirEmprestimoForm(FlaskForm):

    """
    Classe responsável por represntar os campos de preenchimento durante a requisição de empréstimo.

    Atributos:
        Todos os atributos com "campo" em sua descrição devem ser preenchidos pelo usuário.
        Todos os campos devem ser obrigatóriamente preenchidos para que possa se entrar numa conta. 

        valor: Campo para o valor do empréstimo 

        parcelas: Lista de valores que representam o número de parcelas que o usuário pode escolher
        para pagar seu empréstimo

        salario: Campo para o valor do salário do usuário 

        submit: Botão que deve ser apertado pelo usuário após o preenchimento de todos os dados
        anteriores, é usado para ativar a verificação dos dados e, se estiverem corretos, inserir
        os dados do empréstimo no banco de dados
    """

    valor = DecimalField('Valor do empréstimo (R$):',
        validators=[DataRequired(message='O preenchimento deste campo é obrigatório'),
        NumberRange(min=1000, max=20000, message='O valor mínimo para emprestimos é R$ 1000.00 e o máximo R$ 20000.00')])

    parcelas = SelectField('Quantidade de parcelas:',
        choices=[
            (12, '12'),
            (18, '18'),
            (24, '24'),
            (30, '30'),
            (36, '36')
        ])

    salario = DecimalField('Sua renda mensal:',
        validators=[
        NumberRange(min=0, max=100000)])

    submit = SubmitField('Confirmar pedido')

class ConfirmarEmprestimoForm(FlaskForm):

    """
    Classe responsável por represntar os campos de revisão durante a requisição de empréstimo.
    Usada para criar uma instância da classe Emprestimo no banco de dados.

    Atributos:
        Todos os atributos com "campo" em sua descrição devem ser preenchidos pelo usuário.
        Todos os campos devem ser obrigatóriamente preenchidos para que possa se entrar numa conta. 

        valor: Campo para o valor do empréstimo 

        parcelas: Lista de valores que representam o número de parcelas que o usuário pode escolher
        para pagar seu empréstimo

        salario: Campo para o valor do salário do usuário 

        submit: Botão que deve ser apertado pelo usuário após o preenchimento de todos os dados
        anteriores, é usado para ativar a verificação dos dados e, se estiverem corretos, inserir
        os dados do empréstimo no banco de dados
    """

    valor = DecimalField('Valor do empréstimo (R$):')

    parcelas = IntegerField('Quantidade de parcelas:')

    salario = DecimalField('Sua renda mensal:')

    valor_a_pagar = DecimalField('Valor total a ser pago (com juros)')
    
    valor_parcela = DecimalField('Valor a ser pago em cada parcela')

    submit = SubmitField('Confirmar')
