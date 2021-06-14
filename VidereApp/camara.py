from flask import request, Response, Blueprint, render_template, url_for, session
from werkzeug.utils import redirect
import app
import utilizador

camara_pagina = Blueprint('camara', __name__, template_folder='templates')


@camara_pagina.route('/cm<string:feed>', methods=["POST", "GET"])
def janelaCamara(feed):
    if "user_id" in app.session:
        if request.method == "POST":
            r = request.json
            v = r['valor']
            print(v)
            brilho = round(int(v) * 255 / 100)
            utilizador.obtemCrm(session["user_id"], feed).brilho = brilho

            return Response(status=200)
        else:
            # Obtem Nome da Transmissão
            nome = utilizador.obtemCrm(session["user_id"], feed).nome

            return render_template("camara.html", vd_id=feed, camara_nome=nome)
    return redirect(url_for("login"))
