from bd.models import Empresa
from bd.conexao import db

class Acoes():
    def __int__(self):
        pass

    def excluir(self, id_usuario, id_empresa,cnpj):
        try:
            empresa = Empresa.query.get(id_empresa)
            autorizado = empresa.usuario_id
            if id_usuario == autorizado:
                empresa.delete()
                db.session.commit()
                resp = {
                    "status": f'Empresa {cnpj} deletada com sucesso!',
                    "situacao": 'sucesso'
                }
                return resp
            else:
                resp = {
                    "status": 'Acesso negado!',
                    "situacao": 'erro'
                }
                return resp
        except Exception as e:
            resp = {
                "status": f'Erro {e}',
                "situacao": 'erro'
            }
            return resp

    def criar(self, id_usuario, cnpj, cnae, nomeFantasia, nomeRazao):
        jaExiste = Empresa.query.filter_by(cnpj=cnpj).first()
        if jaExiste:
            resp = {
                "status": 'Empresa já cadastrada em nosso sistema!',
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

    def atualizar(self, id_usuario, id_empresa,cnae, nome_fantasia):
        id = id_empresa
        empresa = Empresa.query.get(id)
        autorizado = empresa.usuario_id
        if autorizado == id_usuario:
            empresa.nomeFantasia = nome_fantasia
            empresa.cnae = cnae
            db.session.commit()
            resp = {
                "status": 'Empresa atualizada com sucesso!',
                "situacao": 'sucesso'
            }
            return resp
        else:
            resp = {
                "status": 'Erro, acesso negado!',
                "situacao": 'erro',
                "usuario": id_usuario,
                "empresa": id_empresa
            }
            return resp




