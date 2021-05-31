from flask import Blueprint, request, render_template, url_for
from werkzeug.utils import redirect

import app as main
import dataset
import utilizador
import videredb

novaCamara_pagina = Blueprint('novaCamara', __name__, template_folder='templates')


@novaCamara_pagina.route('/novacamara', methods=["POST", "GET"])  # obtem a galeria
def novaCamaraStream():
    if "user_id" in main.session:

        if request.method == "POST":
            if "novacmr" in request.form:
                if main.session["user_id"] in utilizador.UTILIZADORES_ATIVOS:
                    utilizador.UTILIZADORES_ATIVOS[main.session["user_id"]].IniciaCamara("video.mp4")
                return redirect(url_for("painel"))
        else:
            return render_template("novaCamara.html")
            
    return redirect(url_for("login"))
