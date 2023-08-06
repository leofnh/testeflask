from bd.conexao import db, app
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(555), nullable=False)
    senha_hash = db.Column(db.String(255), nullable=False)
    nomeUsuario = db.Column(db.String(18), nullable=False)

    def set_senha(self, senha):
        self.senha_hash = bcrypt.generate_password_hash(senha).decode('utf-8')

    def verificar_senha(self, senha):
        return bcrypt.check_password_hash(self.senha_hash, senha)

class Empresa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cnpj = db.Column(db.String(18), nullable=False)
    nomeRazao = db.Column(db.String(555))
    nomeFantasia = db.Column(db.String(555))
    cnae = db.Column(db.String(555))
    usuario_id = db.Column(db.String(555))