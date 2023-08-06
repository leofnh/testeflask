from bd.conexao import app, db
from flask import jsonify, request
from bd.models import Usuario, Empresa
from funcoes import cadastroEmpresa, atualizarEmpresa, removerEmpresa, cadastrarUsuario, EmpresaAcoes

@app.route('/')
def home():
    empresas = Empresa.query.all()
    empresa_serial = []
    for empresa in empresas:
        empresa_serials = {
            "id":empresa.id,
            "cnpj":empresa.cnpj
        }
        empresa_serial.append(empresa_serials)
    resp = {
        "status":'Ok agora!',
        "empresa": empresa_serial
    }
    return jsonify(resp)

@app.route('/empresasdados', methods=['GET', 'POST'])
def dadosEmpresa():
    if request.method == 'GET':
        resp = {
            "status":'Metodo inválido',
            "situacao": 'erro'
        }
        return jsonify(resp)
    elif request.method == 'POST':
        empresas = Empresa.query.all()
        dados = {
                    "empresas": [
                        {
                            "cnpj": empresas.cnpj,
                            "id":empresas.id,
                        }
                        for empresas in empresas
                    ],
                    "paginacao": 1,
                    "situacao": 'sucesso'
                }
        return jsonify(dados)

    else:
        resp = {
            "status": 'Metodo inválido',
            "situacao": 'erro'
        }
        return jsonify(resp)

@app.route('/logar', methods=['GET', 'POST'])
def logarapp():
    if request.method == 'POST':
        usuario = request.form.get('usuario')
        senha = request.form.get('senha')
        try:
            if usuario and senha:
                usuarioLogando = Usuario.query.filter_by(nomeUsuario=usuario).first()
                if usuarioLogando and usuarioLogando.verificar_senha(senha):
                    resp = {
                        "status": 'Logado com sucesso!',
                        "situacao": 'sucesso'
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
        nomeRazao = request.form.get('nomeRazao')
        nomeFantasia = request.form.get('nomeFantasia')
        cnpj = request.form.get('cnpj')
        cnae = request.form.get('cnae')
        id_usuario = request.form.get('id_usuario')
        cadastro = cadastroEmpresa.CadastrarEmpresa().cadastrar(nomeFantasia, nomeRazao, cnpj, cnae, id_usuario)
        return jsonify(cadastro)
    else:
        resp = {
            "status": 'Metodo inválido',
            "situacao": 'erro'
        }
        return jsonify(resp)

@app.route('/remover-empresa', methods=['POST', 'GET'])
def removeempresa():
    if request.method == 'POST':
        id_usuario = request.form.get('id_usuario')
        cnpj = request.form.get('cnpj')
        dados_empresa = Empresa.query.get(cnpj=cnpj)
        autorizado = dados_empresa.usuario_id
        if id_usuario == autorizado:
            excluir = removerEmpresa.removerEmpresa().excluirEmpresa(cnpj)
            return jsonify(excluir)
        else:

            resp = {
                "status": 'Acesso negado! Você não tem autorização para remover esta empresa!',
                "situacao": 'erro'
            }
            return jsonify(resp)

    else:
        resp = {
            "status": 'Metodo inválido',
            "situacao": 'erro'
        }
        return jsonify(resp)

@app.route('/editar-empresa', methods=['POST', 'GET'])
def editarempresa():
    if request.method == 'POST':
        id_usuario = request.form.get('id_usuario')
        cnpj = request.form.get('cnpj')
        dados_empresa = Empresa.query.get(cnpj=cnpj)
        autorizado = dados_empresa.usuario_id
        if id_usuario == autorizado:
            idEmpresa = request.form.get('idEmpresa')
            nomeFantasiaAtt = request.args.get('nomefantasia')
            cnaeAtt = request.args.get('cnae')
            atualizar = atualizarEmpresa.atualizarEmpresa().attEmpresa(idEmpresa, nomeFantasiaAtt, cnaeAtt)
            return jsonify(atualizar)
        else:
            resp = {
                "status": 'Acesso negado! Você não tem autorização para remover esta empresa!',
                "situacao": 'erro'
            }
            return jsonify(resp)
    else:
        resp = {
            "status": 'Metodo inválido',
            "situacao": 'erro'
        }
        return jsonify(resp)

@app.route('/acoes-empresas/<int:id_usuario>/<int:id_empresa>', methods=['PUT', 'DELETE', 'POST', 'GET'])
def acoes(id_usuario, id_empresa):
    if request.method == 'PUT':
        cnae = request.json.get('cnae')
        nome_fantasia = request.json.get('nome_fantasia')
        resp = EmpresaAcoes.Acoes().atualizar(id_usuario, id_empresa,cnae, nome_fantasia)
        return jsonify(resp)

    elif request.method == 'GET':
        empresas = Empresa.query.all()
        dados = {
            "empresas": [
                {
                    "cnpj": empresas.cnpj,
                    "id": empresas.id,
                    "usuario": empresas.usuario_id
                }
                for empresas in empresas
            ],
            "paginacao": 1,
            "situacao": 'sucesso'
        }
        return jsonify(dados)

    elif request.method == 'POST':
        cnpj = request.json.get('cnpj')
        cnae = request.json.get('cnae')
        nome_fantasia = request.json.get('nome_fantasia')
        nome_razao = request.json.get('nome_razao')
        resp = EmpresaAcoes.Acoes().criar(id_usuario, cnpj, cnae, nome_fantasia, nome_razao)
        return jsonify(resp)

    elif request.method == 'DELETE':
        cnpj = request.json.get('cnpj')
        resp = EmpresaAcoes.Acoes().excluir(id_usuario, id_empresa, cnpj)
        return jsonify(resp)

    else:
        resp = {
            "status": 'Erro!',
            "metodo": request.method
        }
        return jsonify(resp)

