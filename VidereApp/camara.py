from flask import request, Response, Blueprint, render_template, url_for
from werkzeug.utils import redirect

import app
camara_pagina = Blueprint('camara', __name__, template_folder='templates')


@camara_pagina.route('/cm<string:feed>', methods=["POST", "GET"])
def janelaCamara(feed):
    if "user" in app.session:
        if request.method == "POST":
            r = request.json
            v = r['valor']
            print(v)
            return Response(status=200)
        else:
            return render_template("camara.html", vd_id=feed)
    return redirect(url_for("login"))
