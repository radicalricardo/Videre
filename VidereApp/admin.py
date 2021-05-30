from flask import request, Response, Blueprint, render_template, url_for
from werkzeug.utils import redirect
import app
import videredb

admin_pagina = Blueprint('admin', __name__, template_folder='templates')

@admin_pagina.route('/admin', defaults={'tabela': 'object'})
@admin_pagina.route('/admin/<string:tabela>', methods=["POST", "GET", "PUT", "DELETE"])
def janelaAdmin(tabela):
    if "user_id" in app.session:
        if request.method == "POST":
            pass
        if request.method == "PUT":
            pass
        if request.method == "DELETE":
            pass

        newTabela = videredb.selectTabela(tabela)
        return render_template("admin.html", tabelas=videredb.videreMETA.sorted_tables, tabela=newTabela)

    return redirect(url_for("login"))
