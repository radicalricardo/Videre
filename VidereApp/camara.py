import json

from flask import request, Response, Blueprint, render_template, url_for, session
from werkzeug.utils import redirect
import app
import dataset
import utilizador

camara_pagina = Blueprint('camara', __name__, template_folder='templates')


@camara_pagina.route('/cm<string:feed>', methods=["POST", "GET"])
def janelaCamara(feed):
    if "user_id" in app.session:
        if request.method == "POST":
            r = request.json

            if r['tipo'] == "b":
                per = r['valor']
                brilho = round(int(per) * 255 / 100)
                utilizador.obtemCrm(session["user_id"], feed).brilho = brilho
            elif r['tipo'] == "c":
                per = r['valor']
                contraste = round(int(per) * 255 / 100)
                utilizador.obtemCrm(session["user_id"], feed).contraste = contraste
            elif r['tipo'] == "f":
                filtros_selecionados = r['valor']
                utilizador.obtemCrm(session["user_id"], feed).filtros = list(map(int, filtros_selecionados))
            elif r['tipo'] == "a": # Apaga Video
                utilizador.ApagaCamara(session["user_id"], feed)
                redirect(url_for("painel"))

            return Response(status=200)
        else:
            # Obtem Dados
            cmr = utilizador.obtemCrm(session["user_id"], feed)
            return render_template("camara.html", vd_id=feed, camara_nome=cmr.nome, brilho=cmr.brilho,
                                   contraste=cmr.contraste, classes=dataset.classes,
                                   selecionados=json.dumps(cmr.filtros))
    return redirect(url_for("login"))
