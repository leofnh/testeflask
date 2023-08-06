from bd.conexao import db
from bd.models import Empresa
class CadastrarEmpresa():
    def __init__(self):
        pass

    def cadastrar(self, nomeFantasia, nomeRazao, cnpj, cnae, id_usuario):
        try:
            existeEmpresa = Empresa.query.filter_by(cnpj=cnpj).first()
            if existeEmpresa:
                resp = {
                    "status":'Essa empresa ja foi cadastrada em nosso sistema!',
                    "situacao": 'erro'
                }
                return resp
            else:
                cadastroEmpresa = Empresa(
                    nomeFantasia=nomeFantasia,
                    nomeRazao=nomeRazao,
                    cnpj=cnpj,
                    cnae=cnae,
                    usuario_id=id_usuario
                )
                db.session.add(cadastroEmpresa)
                db.session.commit()

                resp = {
                    "status": f'A empresa {nomeFantasia} foi cadastrada com sucesso! CNPJ: {cnpj}',
                    "situacao": 'sucesso'
                }
                return resp

        except Exception as e:

            resp = {
                "status": f'Houve um erro durante o cadastro {e}',
                "situacao": 'erro'
            }
            return resp
