from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, PasswordField
from wtforms.validators import DataRequired, Length, EqualTo, Email, ValidationError
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