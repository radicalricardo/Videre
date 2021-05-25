from flask import Flask, render_template, Response, request, redirect, url_for, session, send_file, flash
import utilizador
import videredb
from camara import camara_pagina

app = Flask(__name__)
app.register_blueprint(camara_pagina)
app.static_folder = 'static'
app.secret_key = "mdkifk093hrc0384"


# CAMARAS ESTÃO TODAS COM THREAD
# TODO: MOVER FUNÇÕES DE PROCESSAMENTO DE IMAGEM E DA CAMARA PARA UM FICHEIRO DEDICADO
# TODO: ACABAR A PAGINA DA CAMARA

@app.route('/', methods=["POST", "GET"])
def login():
    if request.method == "POST":
        user = request.form["userNome"]
        passworduser = request.form["userSenha"]

        user_id = videredb.verificaUtilizador(user, passworduser)
        if user_id is not None:
            # Mover estas duas linhas para outro lado, utilizador só deverá iniciar um objeto de si proprio quando existir pelo menos um processo
            u = utilizador.Utilizador(user)
            utilizador.UTILIZADORES_ATIVOS[user] = u
            session["user"] = user
            session["user_id"] = user_id
            return redirect(url_for("painel"))
        else:
            flash("Credenciais inválidas")
            return redirect(url_for("login"))

    return render_template("login.html")  # Se for GET


@app.route('/painel', methods=["POST", "GET"])  # Painel de controlo do utilizador
def painel():
    if "user" not in session:  # Se utilizador não tiver ligado
        return redirect(url_for("login"))

    vds_id = []
    if request.method == "POST":
        if "novacmr" in request.form:  # Inicia um novo video (Apenas de testes de momento)
            if session["user"] in utilizador.UTILIZADORES_ATIVOS:
                utilizador.UTILIZADORES_ATIVOS[session["user"]].iniciaVideo("video.mp4")
            return redirect(url_for("painel"))  # Post/Redirect/Get https://en.wikipedia.org/wiki/Post/Redirect/Get
    elif request.method == "GET":
        if session["user"] in utilizador.UTILIZADORES_ATIVOS:
            vds_id = utilizador.UTILIZADORES_ATIVOS.get(session["user"]).videos.keys()
        return render_template("painel.html", vds_id=list(vds_id))


@app.route('/vd<string:feed>')
def transmitirImagem(feed):
    # Obtem video de uma camara de um utilizador, de momento o video é privado
    if "user" in session:
        return Response(utilizador.obtemCrm(session["user"], feed).obtemFrame(),
                        mimetype='multipart/x-mixed-replace; boundary=frame')
    else:
        return redirect(url_for("login"))


@app.route('/tb<string:feed>')  # Obtem thumbnail
def transmitirthumbnail(feed):
    if "user" in session:
        tb = utilizador.obtemCrm(session["user"], feed).obtemThumbnail()
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
    session.pop("user", None)
    return redirect(url_for("login"))
