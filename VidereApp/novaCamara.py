from flask import Blueprint, request, render_template, url_for, flash
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
                    linkCamara = request.form["linkCamara"].strip()
                    nomeCamara = request.form["nomeCamara"].strip()
                    # if linkCamara == "TESTE": linkCamara = "video.mp4"  # USADO PARA TESTES

                    filtroObjetos = []
                    for i in dataset.classes.keys():
                        if request.form.get(str(i)) == "on":
                            filtroObjetos.append(i)

                    erros = 0
                    if not linkCamara:
                        flash("Link da câmera vazio. É necessário inserir um.")
                        erros += 1
                    if not nomeCamara:
                        flash("Nome da câmera vazio. É necessário inserir um.")
                        erros += 1
                    if len(filtroObjetos) == 0:
                        flash("Não há nenhum objeto selecionado para instruir a detectação.")
                        erros += 1
                    if utilizador.ObtemExistenciaCmr(main.session["user_id"], nomeCamara):
                        flash("Já existe uma câmera com este nome.")
                        erros += 1
                    if erros > 0: return redirect(url_for("novaCamara.novaCamaraStream"))

                    utilizador.UTILIZADORES_ATIVOS[main.session["user_id"]].CriaCamara(linkCamara, nomeCamara, filtroObjetos)
                return redirect(url_for("painel"))
        else:
            return render_template("novaCamara.html", classes=dataset.classes)

    return redirect(url_for("login"))
