import json

from flask import Flask, render_template, Response, request, redirect, url_for, session, send_file, flash, \
    send_from_directory
import config
import utilizador
import videredb
from camara import camara_pagina
from galeria import galeria_pagina
from admin import admin_pagina
from carregarFicheiros import carregarFicheiros_pagina
from novaCamara import novaCamara_pagina

app = Flask(__name__)
app.register_blueprint(camara_pagina)
app.register_blueprint(galeria_pagina)
app.register_blueprint(admin_pagina)
app.register_blueprint(novaCamara_pagina)
app.register_blueprint(carregarFicheiros_pagina)
app.static_folder = 'static'
app.secret_key = config.chaveSession


@app.route('/', methods=["POST", "GET"])
def login():
    if "user_id" in session:
        return redirect(url_for("painel"))

    if request.method == "POST":
        user_nome = request.form["userNome"].strip()
        passworduser = request.form["userSenha"].strip()

        user_id = videredb.verificaUtilizador(user_nome, passworduser)
        if user_id is not None:
            if user_id not in utilizador.UTILIZADORES_ATIVOS:
                u = utilizador.Utilizador(user_id)
                utilizador.UTILIZADORES_ATIVOS[user_id] = u
            session["user_nome"] = user_nome
            session["user_id"] = user_id
            return redirect(url_for("painel"))
        else:
            flash("Credenciais inválidas")
            return redirect(url_for("login"))

    return render_template("login.html")  # Se for GET


@app.route('/registo', methods=["POST", "GET"])
def registo():
    if "user_id" not in session:
        if request.method == "POST":
            user_nome = request.form["nomeUser"].strip()
            senha = request.form["senhaUser"].strip()

            if not len(user_nome) > 0:
                flash("Nome de utilizador está vazio.")
                return redirect(url_for("registo"))

            if not videredb.verificaDisponibilidadeUser(user_nome):
                flash("Este utilizador já existe")
                return redirect(url_for("registo"))

            if not len(senha) > 5:
                flash("A senha precisa de ter mais que 5 caracteres.")
                return redirect(url_for("registo"))

            videredb.inserirUtilizador(user_nome, senha)
            return redirect(url_for("login"))
        else:
            return render_template("registo.html")
    else:
        return redirect(url_for("painel"))


@app.route('/painel', methods=["POST", "GET"])  # Painel de controlo do utilizador
def painel():
    if "user_id" not in session:  # Se utilizador não tiver ligado
        return redirect(url_for("login"))

    vds_id = []
    if request.method == "POST":
        if "novacmr" in request.form:  # Inicia um nova camara
            return redirect(url_for("novaCamara.novaCamaraStream"))

    elif request.method == "GET":
        if session["user_id"] in utilizador.UTILIZADORES_ATIVOS:
            vds_id = utilizador.UTILIZADORES_ATIVOS.get(session["user_id"]).obtemCamarasLigacao()
        return render_template("painel.html", vds_id=vds_id)


@app.route('/pg<string:feed>')
def progressoProcessoVideo(feed):
    if "user_id" in session:
        try:
            dado = utilizador.obtemVideo(session["user_id"], feed).progresso()
            return json.dumps({'progresso': dado}), 200, {'ContentType': 'application/json'}
        except:
            return json.dumps({'progresso': -1}), 200, {'ContentType': 'application/json'}
    else:
        return redirect(url_for("login"))


# ==============================================================

@app.route('/video<string:feed>')  # Pagina de resultado de video em ficheiro procesado
def VideoPaginaProcesso(feed):
    if "user_id" in session:
        return render_template("videoResultado.html", feed=feed)
    else:
        return redirect(url_for("login"))


@app.route('/vdc<string:feed>')  # Video mp4 do ficheiro carregado processado
def videoProcessadoResultado(feed):
    if "user_id" in session:
        return send_from_directory(config.pastaVideos, feed + '.webm')
    else:
        return redirect(url_for("login"))


# ==============================================================

@app.route('/vd<string:feed>')  # Video para transmissão das camaras
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


@app.route('/sobre')
def sobre():
    if "user_id" in session:
        return render_template("sobre.html", barra=True)
    else:
        return render_template("sobre.html", barra=False)


@app.route('/terminarsessao')
def desligar():
    session.clear()
    # session.pop("user_id", None)
    return redirect(url_for("login"))
