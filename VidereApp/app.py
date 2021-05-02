import io

from flask import Flask, render_template, Response, request, redirect, url_for, session, send_file
import utilizador

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
        print(request)
        user = request.form["userNome"]
        session["user"] = user

        # PARA TESTES
        u = utilizador.Utilizador(user)
        utilizador.UTILIZADORES_ATIVOS.append(u)
        print(utilizador.UTILIZADORES_ATIVOS)

        return redirect(url_for("painel"))
    else:
        return render_template("login.html")


@app.route('/painel', methods=["POST", "GET"])  # Painel de controlo do utilizador
def painel():
    if "user" not in session:  # Se utilizador não tiver ligado
        return redirect(url_for("login"))

    if request.method == "POST":
        vds_id = []
        if "novacmr" in request.form:  # Inicia um novo video (Apenas de testes de momento)
            for i in utilizador.UTILIZADORES_ATIVOS:
                if i.id == session["user"]:
                    i.iniciaVideo(0)
        for i in utilizador.UTILIZADORES_ATIVOS:
            if i.id == session["user"]:
                vds_id = i.videos
        return render_template("painel.html", vds_id=vds_id)
    elif request.method == "GET":
        return render_template("painel.html")


@app.route('/vd<string:feed>')
def transmitirImagem(feed):
    # Obtem video de uma camara de um utilizador, de momento o video é privado
    if "user" in session:
        return Response(utilizador.obtemUser(session["user"], feed).obtemFrame(),
                        mimetype='multipart/x-mixed-replace; boundary=frame')
    else:
        return redirect(url_for("login"))


@app.route('/tb<string:feed>')  # Obtem Tumbnail
def transmitirTumbNail(feed):
    if "user" in session:
        tb = utilizador.obtemUser(session["user"], feed).obtemTumbnail()
        if tb is None: # Se não houver frames disponiveis, retorna uma imagem comum de loading
            return redirect(url_for('static', filename='img/eyetumb.png'))
        else:
            return Response(tb, mimetype='multipart/x-mixed-replace; boundary=frame')
    else:
        return redirect(url_for("login"))


@app.route('/camara')
def janelaCamara():
    pass


@app.route('/terminarsessao')
def desligar():
    session.pop("user", None)
    return redirect(url_for("login"))
