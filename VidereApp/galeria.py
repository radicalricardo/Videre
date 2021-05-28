from flask import request, Blueprint, render_template, url_for
from VidereApp import dataset

galeria_pagina = Blueprint('galeria', __name__, template_folder='templates')

@galeria_pagina.route('/galeria', methods=["POST", "GET"])  # obtem a galeria
def janelaGaleria():
    if request.method == "POST":
        pass
    return render_template("galeria.html", classes=list(dataset.classes.values()))  # Se for GET