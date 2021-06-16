from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, PasswordField
from wtforms.validators import DataRequired, Length, EqualTo 

class CadastrarUsuarioForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired(), Length(min=2, max=50)])
    
    cpf = StringField('CPF (somente números)', validators=[DataRequired(), Length(min=11, max=11)])

    senha = PasswordField('Senha', validators=[DataRequired()])
    confirmar_senha = PasswordField('Confirmar Senha', validators=[DataRequired(), EqualTo('senha')])

    submit = SubmitField('Cadastrar')


class LoginForm(FlaskForm):
    
    cpf = StringField('CPF (somente números)', validators=[DataRequired(), Length(min=11, max=11)])

    senha = PasswordField('Senha', validators=[DataRequired()])

    lembrar = BooleanField('Lembrar usuário')

    submit = SubmitField('Entrar')