from bd.conexao import app
from flask import jsonify, request
from bd.models import Usuario, Empresa
from funcoes import cadastroEmpresa, cadastrarUsuario, EmpresaAcoes
from flask_restful import Api, Resource

api = Api(app)

@app.route('/logar', methods=['GET', 'POST'])
def logarapp():
    if request.method == 'POST':
        usuario = request.form.get('usuario')
        senha = request.form.get('senha')
        try:
            if usuario and senha:
                usuarioLogando = Usuario.query.filter_by(nomeUsuario=usuario).first()
                if usuarioLogando and usuarioLogando.verificar_senha(senha):
                    id_usuario = usuarioLogando.id
                    resp = {
                        "status": 'Logado com sucesso!',
                        "situacao": 'sucesso',
                        "id_usuario": id_usuario
                    }
                    return jsonify(resp)
                else:

                    resp = {
                        "status": 'Erro com usuário ou senha, tente outra vez!',
                        "situacao": 'erro'
                    }
                    return jsonify(resp)
        except Exception as e:
            resp = {
                "status": f'erro: {e}',
                "situacao": 'erro'
            }
            return jsonify(resp)
    else:
        resp = {
            "status": 'Metodo inválido',
            "situacao": 'erro'
        }
        return jsonify(resp)

@app.route('/cadastro-usuario', methods=['GET', 'POST'])
def cadastrouser():
    if request.method == 'POST':
        usuario = request.form.get('usuario')
        senha = request.form.get('senha')
        if usuario and senha:
            cadastro = cadastrarUsuario.cadastroUsuario().novoUsuario(usuario, senha)
            return jsonify(cadastro)
        else:
            resp = {
                "status": 'Digite o usuário e senha!',
                "situacao": 'erro'
            }
            return jsonify(resp)
    else:
        resp = {
            "status": 'Metodo inválido',
            "situacao": 'erro'
        }
        return jsonify(resp)

@app.route('/cadastro-empresa', methods=['GET', 'POST'])
def cadastroempresa():
    if request.method == 'POST':
        nomeRazao = request.json.get('nomeRazao')
        nomeFantasia = request.json.get('nomeFantasia')
        cnpj = request.json.get('cnpj')
        cnae = request.json.get('cnae')
        id_usuario = request.json.get('id_usuario')
        cadastro = cadastroEmpresa.CadastrarEmpresa().cadastrar(nomeFantasia, nomeRazao, cnpj, cnae, id_usuario)
        return jsonify(cadastro)
    else:
        resp = {
            "status": 'Metodo inválido',
            "situacao": 'erro'
        }
        return jsonify(resp)

class AcoesEmpresa(Resource):
    def put(self, id_usuario, id_empresa):
        cnae = request.json.get('cnae')
        nome_fantasia = request.json.get('nome_fantasia')
        resp = EmpresaAcoes.Acoes().atualizar(id_usuario, id_empresa,cnae, nome_fantasia)
        return resp
    def get(self, id_usuario, id_empresa):
        empresas = Empresa.query.all()
        dados = {
            "empresas": [
                {
                    "cnpj": empresas.cnpj,
                    "id": empresas.id,
                    "usuario": empresas.usuario_id,
                    "cnae":empresas.cnae,
                    "nomeRazao:":empresas.nomeRazao,
                    "nomeFantasia":empresas.nomeFantasia
                }
                for empresas in empresas
            ],
            "paginacao": 1,
            "situacao": 'sucesso'
        }

        return dados

    def delete(self, id_usuario, id_empresa):
        cnpj = request.json.get('cnpj')
        resp = EmpresaAcoes.Acoes().excluir(id_usuario, id_empresa, cnpj)
        return resp

    def post(self, id_usuario, id_empresa):
        cnpj = request.json.get('cnpj')
        cnae = request.json.get('cnae')
        nome_fantasia = request.json.get('nome_fantasia')
        nome_razao = request.json.get('nome_razao')
        resp = EmpresaAcoes.Acoes().criar(id_usuario, cnpj, cnae, nome_fantasia, nome_razao)
        return resp


api.add_resource(AcoesEmpresa, '/acoes-empresas-teste/<int:id_usuario>/<int:id_empresa>')




