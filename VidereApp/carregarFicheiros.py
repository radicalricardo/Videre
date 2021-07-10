import os
import uuid

import cv2
import numpy
from flask import Blueprint, request, render_template, url_for, flash, session, Response
from werkzeug.utils import redirect

import dataset
import utilizador

carregarFicheiros_pagina = Blueprint('carregaFicheiro', __name__, template_folder='templates')


@carregarFicheiros_pagina.route('/carregar', methods=["POST", "GET"])
def carregaFicheiros():
    if "user_id" in session:
        filtroObjetos = []
        if request.method == "POST":
            if 'file' not in request.files:
                flash('Pedido feito não possui ficheiro.')
                return redirect(url_for("carregaFicheiro.carregaFicheiros"))

            file = request.files['file']
            if file.filename == '':
                flash('Nenhum ficheiro selecionado')
                return redirect(url_for("carregaFicheiro.carregaFicheiros"))

            if file and not file.filename.lower().endswith(('.png', '.jpg', '.jpeg', '.mp4')):
                flash('Formato do ficheiro não é suportado. Use apenas PNG, JPG, JPEG ou MP4')
                return redirect(url_for("carregaFicheiro.carregaFicheiros"))

            for i in dataset.classes.keys():
                if request.form.get(str(i)) == "on":
                    filtroObjetos.append(i)

            if len(filtroObjetos) == 0:
                flash("Não há nenhum filtro selecionado para iniciar a detectação.")
                return redirect(url_for("carregaFicheiro.carregaFicheiros"))

            if not file.filename.lower().endswith('mp4'):  # É uma imagem
                frame = cv2.imdecode(numpy.frombuffer(request.files['file'].read(), numpy.uint8), cv2.IMREAD_UNCHANGED)
                link = utilizador.UTILIZADORES_ATIVOS[session["user_id"]].CriaProcessoImagem(frame, filtroObjetos)
                return redirect("/verimagem/" + link)

            else:  # É um video
                vid = str(uuid.uuid1()).replace("-", "")  # Gera um nome para o ficheiro que vai servir como ID
                file.save(os.path.join(vid + ".mp4"))
                utilizador.UTILIZADORES_ATIVOS[session["user_id"]].CriaProcessoVideo(vid, filtroObjetos)
                return redirect("/video" + vid)
        else:
            return render_template("carregarFicheiro.html", classes=dataset.classes)
    else:
        return redirect(url_for("login"))
