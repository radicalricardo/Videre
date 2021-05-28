from flask import request, Blueprint, render_template, url_for
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
        return render_template("galeria.html", classes=list(dataset.classes.values()), fotos=fotos)  # Se for GET

    return redirect(url_for("login"))

