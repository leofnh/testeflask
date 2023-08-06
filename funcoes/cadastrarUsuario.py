from bd.models import Usuario
from bd.conexao import db

class cadastroUsuario():
    def __init__(self):
        pass

    def novoUsuario(self, usuario, senha):
        try:
            jaExiste = Usuario.query.filter_by(nomeUsuario=usuario).first()
            if jaExiste:
                resp = {
                    "status": 'Este usuário já está cadastrado!',
                    "situacao": 'erro'
                }
                return resp
            else:
                novoCadastro = Usuario(nome=usuario, nomeUsuario=usuario)
                novoCadastro.set_senha(senha)
                db.session.add(novoCadastro)
                db.session.commit()
                resp = {
                    "status": 'Bem vindo, você acaba de se cadastrar!',
                    "situacao": 'sucesso'
                }
                return resp

        except Exception as e:
            resp = {
                "status": f'Erro durante o cadastro, {e}',
                "situacao": 'erro'
            }
            return resp