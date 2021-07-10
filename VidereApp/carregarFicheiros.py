import os
import uuid

import cv2
import numpy
from flask import Blueprint, request, render_template, url_for, flash, session, Response
from werkzeug.utils import redirect

import utilizador

carregarFicheiros_pagina = Blueprint('carregaFicheiro', __name__, template_folder='templates')


@carregarFicheiros_pagina.route('/carregar', methods=["POST", "GET"])
def carregaFicheiros():
    if "user_id" in session:

        if request.method == "POST":
            if 'file' not in request.files:
                flash('Pedido feito não possui ficheiro.')
                return redirect(url_for("inicio"))

            file = request.files['file']
            if file.filename == '':
                flash('Nenhum ficheiro selecionado')
                return redirect(url_for("inicio"))

            if file and not file.filename.lower().endswith(('.png', '.jpg', '.jpeg', '.mp4')):
                flash('Formato do ficheiro não é suportado. Use apenas PNG, JPG, JPEG ou MP4')
                return redirect(url_for("inicio"))

            if not file.filename.lower().endswith('mp4'):  # É uma imagem
                frame = cv2.imdecode(numpy.frombuffer(request.files['file'].read(), numpy.uint8), cv2.IMREAD_UNCHANGED)
                link = utilizador.UTILIZADORES_ATIVOS[session["user_id"]].CriaProcessoImagem(frame, [0, 1, 2])
                return redirect("/verimagem/" + link)
                # cv2.imwrite('Imagem.jpg', frame)
            else:  # É um video
                vid = str(uuid.uuid1()).replace("-", "")  # Gera um nome para o ficheiro que vai servir como ID
                file.save(os.path.join(vid + ".mp4"))
                utilizador.UTILIZADORES_ATIVOS[session["user_id"]].CriaProcessoVideo(vid,
                                                                                     [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
                                                                                      11, 12, 13, 14, 15, 16, 17, 18,
                                                                                      19, 20, 21, 22, 23, 24, 25, 26,
                                                                                      27, 28, 29, 30, 31, 32, 33, 34,
                                                                                      35, 36, 37, 38, 39, 40, 41, 42,
                                                                                      43, 44, 45, 46, 47, 48, 49, 50,
                                                                                      51, 52, 53, 54, 55, 56, 57, 58,
                                                                                      59, 60, 61, 62, 63, 64, 65, 66,
                                                                                      67, 68, 68, 69, 70, 71, 72, 73,
                                                                                      74, 75, 76, 77, 78, 79, 80])
                # return render_template("videoResultado.html", feed=vid)
                return redirect("/video" + vid)
        else:
            return render_template("carregarFicheiro.html")
    else:
        return redirect(url_for("login"))
