from flask import Flask, render_template, Response, request, redirect, url_for, session, send_file, flash
import utilizador
import videredb

app = Flask(__name__)
app.static_folder = 'static'
app.secret_key = "mdkifk093hrc0384"


# CAMARAS ESTÃO TODAS COM THREAD
# TODO: RESTRUTAR FICHEIROS E PASTAS DO PROJETO PARA O NORMAL DO FLASK
# TODO: CRIAR UM FICHEIRO DE CONFIG.PY COM VARS GLOBAIS DE TODAS AS CONFIGURAÇOES DO SITE (ACESSOS A BDS ECT)
# TODO: FICHEIRO INIT
# TODO: MOVER FUNÇÕES DE PROCESSAMENTO DE IMAGEM E DA CAMARA PARA UM FICHEIRO DEDICADO

@app.route('/', methods=["POST", "GET"])
def login():
    if request.method == "POST":
        user = request.form["userNome"]
        passworduser = request.form["userSenha"]

        if videredb.verificaUtilizador(user, passworduser):
            u = utilizador.Utilizador(user) # Mover estas duas linhas para outro lado, utilizador só deverá iniciar um objeto de si proprio quando existir pelo menos um processo
            utilizador.UTILIZADORES_ATIVOS[user] = u
            session["user"] = user
            return redirect(url_for("painel"))
        else:
            flash("Credenciais inválidas")
            return redirect(url_for("login"))

    return render_template("login.html") # Se for GET


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
                        # tornar isto livre de procura de sessions
                        mimetype='multipart/x-mixed-replace; boundary=frame')
    else:
        return redirect(url_for("login"))


@app.route('/tb<string:feed>')  # Obtem Tumbnail
def transmitirTumbNail(feed):
    if "user" in session:
        tb = utilizador.obtemCrm(session["user"], feed).obtemTumbnail()
        if tb is None:  # Se não houver frames disponiveis, retorna uma imagem comum de loading
            return redirect(url_for('static', filename='img/eyetumb.gif'))
        else:
            return Response(tb, mimetype='multipart/x-mixed-replace; boundary=frame')
    else:
        return redirect(url_for("login"))


@app.route('/cm<string:feed>')
def janelaCamara(feed):
    return render_template("camara.html", vd_id=feed)


@app.route('/sucesso')
def sucessoPainel():
    return redirect(url_for("painel"))


@app.route('/terminarsessao')
def desligar():
    session.pop("user", None)
    return redirect(url_for("login"))
