from bd.models import Empresa
from bd.conexao import db
class removerEmpresa():
    def __init__(self):
        pass

    def excluirEmpresa(self, cnpj):
        try:
            empresa = Empresa.query.filter_by(cnpj=cnpj)
            if empresa:
                empresa.delete()
                db.session.commit()
                resp = {
                    "status": 'Empresa deletada com sucesso!',
                    "situacao": 'sucesso'
                }
                return resp
            else:
                resp = {
                    "status": 'Empresa não encontrada',
                    "situacao": 'erro'
                }
                return resp
        except Exception as e:
            resp = {
                "status": f'Houve um erro durante a exclusão da empresa, {e}',
                "situacao": 'erro'
            }
            return resp