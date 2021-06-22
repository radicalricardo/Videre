import os

import cv2
import numpy
from flask import Blueprint, request, render_template, url_for, flash
from werkzeug.utils import redirect

carregarFicheiros_pagina = Blueprint('carregaFicheiro', __name__, template_folder='templates')


@carregarFicheiros_pagina.route('/carregar', methods=["POST", "GET"])
def carregaFicheiros():

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

        if not file.filename.lower().endswith('mp4'): # É uma imagem
            frame = cv2.imdecode(numpy.frombuffer(request.files['file'].read(), numpy.uint8), cv2.IMREAD_UNCHANGED)
            cv2.imwrite('Imagem.jpg', frame)
        else: # É um video
            file.save(os.path.join("videoTeste.mp4"))
        return render_template("carregarFicheiro.html")

    else:
        return render_template("carregarFicheiro.html")
