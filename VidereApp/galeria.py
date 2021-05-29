from flask import request, Blueprint, render_template, url_for, send_from_directory
from werkzeug.utils import redirect
import app as main
import dataset
import videredb

galeria_pagina = Blueprint('galeria', __name__, template_folder='templates')


@galeria_pagina.route('/galeria', methods=["POST", "GET"])  # obtem a galeria
def janelaGaleria():
    if "user_id" in main.session:
        if request.method == "POST":
            pass
        fotos = videredb.obtemFrames(main.session["user_id"])
        return render_template("galeria.html", classes=list(dataset.classes.values()), fotos=list(fotos))

    return redirect(url_for("login"))


@galeria_pagina.route("/foto/<img>")
def obtemFrameGaleria(img):
    if "user_id" in main.session:
        return send_from_directory("Frames", img + ".png")
    return redirect(url_for("login"))
