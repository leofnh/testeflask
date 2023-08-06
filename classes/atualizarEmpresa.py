from bd.conexao import db
from bd.models import Empresa
class atualizarEmpresa():
    def __init__(self):
        pass

    def attEmpresa(self, id, nomeFantasia, cnae):
        try:
            empresa = Empresa.query.get(id)
            if empresa:
                empresa.nomeFantasia = nomeFantasia
                empresa.cnae = cnae
                db.session.commit()
                resp = {
                    "status": 'Empresa atualizada com sucesso!',
                    "situacao":'sucesso'
                }
                return resp
        except Exception as e:
            resp = {
                "status": f'Erro durante atualização do cadastro {e}',
                "situacao": 'erro'
            }
            return resp