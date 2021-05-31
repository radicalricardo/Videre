from flask import Flask, render_template, Response, request, redirect, url_for, session, send_file, flash
import config
import utilizador
import videredb
from camara import camara_pagina
from galeria import galeria_pagina
from admin import admin_pagina
from novaCamara import novaCamara_pagina

app = Flask(__name__)
app.register_blueprint(camara_pagina)
app.register_blueprint(galeria_pagina)
app.register_blueprint(admin_pagina)
app.register_blueprint(novaCamara_pagina)
app.static_folder = 'static'
app.secret_key = config.chaveSession


# TODO: ACABAR A PAGINA DA CAMARA
# TODO: ADAPTAR À ALTERAÇÃO DO DATASET.CLASSES
# TODO: Galeria ainda inacanada, HTML COM BUGS DEIXAR PARA BRUNO
# TODO: NAVBAR BUGADA QUANDO ENCOLHE, Á MESMO BUE TEMPO, DEIXAR PARA BRUNO
# TODO: DAR UMA COR DIFERENTE A CADA QUADRADO
# TODO: PAGINA DE CRIAR CAMARAS EM PROGRESSO


@app.route('/', methods=["POST", "GET"])
def login():
    if request.method == "POST":
        user_nome = request.form["userNome"]
        passworduser = request.form["userSenha"]

        user_id = videredb.verificaUtilizador(user_nome, passworduser)
        if user_id is not None:
            # Mover estas duas linhas para outro lado, utilizador só deverá iniciar um objeto de si proprio quando existir pelo menos um processo
            u = utilizador.Utilizador(user_id)
            utilizador.UTILIZADORES_ATIVOS[user_id] = u
            session["user_nome"] = user_nome
            session["user_id"] = user_id
            return redirect(url_for("painel"))
        else:
            flash("Credenciais inválidas")
            return redirect(url_for("login"))

    return render_template("login.html")  # Se for GET


@app.route('/painel', methods=["POST", "GET"])  # Painel de controlo do utilizador
def painel():
    if "user_id" not in session:  # Se utilizador não tiver ligado
        return redirect(url_for("login"))

    vds_id = []
    if request.method == "POST":
        if "novacmr" in request.form:  # Inicia um novo video (Apenas de testes de momento)
            return redirect(url_for("novaCamara.novaCamaraStream"))
    elif request.method == "GET":
        if session["user_id"] in utilizador.UTILIZADORES_ATIVOS:
            vds_id = utilizador.UTILIZADORES_ATIVOS.get(session["user_id"]).videos.keys()
        return render_template("painel.html", vds_id=list(vds_id))


@app.route('/vd<string:feed>')
def transmitirImagem(feed):
    # Obtem video de uma camara de um utilizador, de momento o video é privado
    if "user_id" in session:
        return Response(utilizador.obtemCrm(session["user_id"], feed).obtemFrame(),
                        mimetype='multipart/x-mixed-replace; boundary=frame')
    else:
        return redirect(url_for("login"))


@app.route('/tb<string:feed>')  # Obtem thumbnail
def transmitirthumbnail(feed):
    if "user_id" in session:
        tb = utilizador.obtemCrm(session["user_id"], feed).obtemThumbnail()
        if tb is None:  # Se não houver frames disponiveis, retorna uma imagem comum de loading
            return redirect(url_for('static', filename='img/eyetumb.gif'))
        else:
            return Response(tb, mimetype='multipart/x-mixed-replace; boundary=frame')
    else:
        return redirect(url_for("login"))


@app.route('/sucesso')
def sucessoPainel():
    return redirect(url_for("painel"))


@app.route('/terminarsessao')
def desligar():
    session.clear()
    # session.pop("user_id", None)
    return redirect(url_for("login"))
