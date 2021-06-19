from flask import Blueprint, request, render_template, url_for, flash
from werkzeug.utils import redirect

carregarFicheiros_pagina = Blueprint('carregaFicheiro', __name__, template_folder='templates')


@carregarFicheiros_pagina.route('/carregar', methods=["POST", "GET"])
def carregaFicheiros():
    return render_template("carregarFicheiro.html")
