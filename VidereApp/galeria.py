from flask import request, Blueprint, render_template, url_for, send_from_directory
from werkzeug.utils import redirect
import app as main
import config
import dataset
import videredb

galeria_pagina = Blueprint('galeria', __name__, template_folder='templates')


@galeria_pagina.route('/galeria', methods=["POST", "GET"])  # obtem a galeria
def janelaGaleria():
    if "user_id" in main.session:
        if request.method == "POST":
            pass
        fotos = videredb.obtemFrames(main.session["user_id"])
        videos = videredb.obtemVideo(main.session["user_id"])
        print(videos)
        return render_template("galeria.html", classes=list(dataset.classes.values()), fotos=fotos, videos=videos)

    return redirect(url_for("login"))


@galeria_pagina.route("/foto/<img>")
def obtemFrameGaleria(img):
    if "user_id" in main.session:
        return send_from_directory(config.pastaFrames, img + ".png")
    return redirect(url_for("login"))


@galeria_pagina.route('/vervideo/<string:feed>',  methods=["POST", "GET"])  # Mostra Video da galaria
def VideoGaleriaVer(feed):
    if "user_id" in main.session:
        if request.method == "GET":
            dono = videredb.seUserDonoVideo(feed, main.session["user_id"])
            return render_template("verVideo.html", feed=feed, dono=dono)

        elif request.method == "POST":
            if "apagavid" in request.form:  # Apaga Video
                videredb.removeVideo(feed, main.session["user_id"])
                return redirect(url_for("galeria.janelaGaleria"))
    else:
        return redirect(url_for("login"))


@galeria_pagina.route('/verimagem/<img>', methods=["POST", "GET"])
def paginaVerImagem(img):
    if "user_id" in main.session:
        if request.method == "GET":
            dono = videredb.seUserDonoFrame(img, main.session["user_id"])
            data = videredb.obtemDadaFrame(main.session["user_id"], img)
            return render_template("verImagem.html", img=img, data=data, dono=dono)

        elif request.method == "POST":
            if "apagaimg" in request.form:  # Apaga Imagem
                if not videredb.removeFrame(img, main.session["user_id"]):
                    return redirect(url_for("login"))
                return redirect(url_for("galeria.janelaGaleria"))
    return redirect(url_for("login"))
