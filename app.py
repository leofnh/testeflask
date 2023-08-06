from bd.conexao import db, app
from classes import cadastroEmpresa, atualizarEmpresa, removerEmpresa, cadastrarUsuario
from flask import render_template, request, jsonify, redirect, flash, session
from bd.models import Empresa, Usuario
from flask_bcrypt import Bcrypt

cript = Bcrypt(app)

@app.route('/')
def vUsuario():
    try:
        logado = session['autenticado']
        if logado:
            return redirect('/cadastro/empresa')
    except:
        return redirect('/logar')

@app.route('/deslogar')
def deslogar():
    logado = session['autenticado']
    if logado:
        session.pop('autenticado', None)
        session.pop('nome_usuario', None)
        session.pop('id_usuario', None)
        return redirect('/logar')
    else:
        return redirect('/logar')


@app.route('/cadastro/empresa', methods=['GET', 'POST'])
def cadastrandoEmpresa():
    if request.method == 'GET':
        empresa = Empresa.query.all()
        dados = {
            "empresa": empresa
        }
        idEmpresa = request.args.get('id')
        if idEmpresa is not None:
            methodInput = request.args.get('metodo')
            if methodInput == 'delete':
                cnpj = request.args.get('cnpj')
                excluir = removerEmpresa.removerEmpresa().excluirEmpresa(cnpj)
                empresaAtt = Empresa.query.all()
                dados['empresa'] = empresaAtt
                dados['status'] = excluir['status']
                dados['situacao'] = excluir['situacao']
                return render_template('home.html', **dados)

            nomeFantasiaAtt = request.args.get('nomefantasia')
            cnaeAtt = request.args.get('cnae')
            atualizar = atualizarEmpresa.atualizarEmpresa().attEmpresa(idEmpresa, nomeFantasiaAtt, cnaeAtt)
            dados['status'] = atualizar['status']
            dados['situacao'] = atualizar['situacao']
            return render_template('home.html', **dados)

        return render_template('home.html', **dados)

    elif request.method == 'POST':
        nomeRazao = request.form.get('nomeRazao')
        nomeFantasia = request.form.get('nomeFantasia')
        cnpj = request.form.get('cnpj')
        cnae = request.form.get('cnae')
        id_usuario = session.get('id_usuario', None)
        print(id_usuario)
        cadastro = cadastroEmpresa.CadastrarEmpresa().cadastrar(nomeFantasia, nomeRazao, cnpj, cnae, id_usuario)
        return jsonify(cadastro)


@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        usuario = request.form.get('usuario')
        senha = request.form.get('senha')

        if usuario is not None and senha is not None:
            cadastro = cadastrarUsuario.cadastroUsuario().novoUsuario(usuario, senha)
            return jsonify(cadastro)
        else:
            pass
    elif request.method == 'GET':
        usuarios = Usuario.query.all()
        dados = {
            "usuarios":usuarios
        }
        return render_template('cadastro.html', **dados)

@app.route('/teste')
def teste():
    if 'autenticado' in session and session['autenticado']:
        nome_usuario = session.get('nome_usuario',
                                   'Usuário')
        id_usuario = session.get('id_usuario', 'Sem ID')
        saudacao = f'Olá, {nome_usuario} - ID: {id_usuario}!'
        return saudacao
    else:
        return 'Acesso não autorizado.'

@app.route('/logar', methods=['GET', 'POST'])
def logando():
    try:
        logado = session['autenticado']
        if logado:
            return redirect('/')
    except:
        pass

    if request.method == 'POST':
        usuario = request.form.get('usuario')
        senha = request.form.get('senha')
        if usuario and senha:
            usuarioLogando = Usuario.query.filter_by(nomeUsuario=usuario).first()
            if usuarioLogando and usuarioLogando.verificar_senha(senha):
                flash('Login realizado com sucesso!', 'success')
                session['autenticado'] = True
                session['nome_usuario'] = usuarioLogando.nomeUsuario
                session['id_usuario'] = usuarioLogando.id
                return redirect('/teste')
            else:
                flash('Usuário ou senha inválido!', 'error')
        else:
            flash('Por favor, forneça usuário e senha.', 'error')

        return redirect('/logar')
    elif request.method == 'GET':
        return render_template('logando.html')
    else:
        return redirect('/logar/')
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)