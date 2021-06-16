from FlaskEmprestimo import db

# Criação das classes que darão origem às tabelas do banco de dados local

class Usuario(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    cpf = db.Column(db.String(11), nullable = False, unique=True)
    senha = db.Column(db.String(60), nullable=False)
    salario = db.Column(db.Integer)
    emprestimos = db.relationship('Emprestimo', backref='beneficiado', lazy=True)

    def __repr__(self):
        return f"Usuário: ('{self.nome}', '{self.cpf}')"

class Emprestimo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    valor = db.Column(db.Integer, nullable=False)
    parcelas = db.Column(db.Integer, nullable=False)
    parcelas_restantes = db.Column(db.Integer, nullable=False)
    valor_parcela = db.Column(db.Integer, nullable=False)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)

    def __repr__(self):
        return f"""Valor: R$ {self.valor}
Parcelas restantes: {self.parcelas_restantes}
Valor à ser pago: {self.valor_parcela * self.parcelas_restantes}"""