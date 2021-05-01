import cv2
import numpy as np
from flask import Flask, render_template, Response
from flask import Flask, session
import time
import utilizador

app = Flask(__name__)
app.secret_key = "senha"


# TODO: TORNAR CAMARAS DO UTILIZADOR NUMA THREAD OU CADA CAMARA NUMA THREAD


@app.route('/video_feed<string:nome>')
def video_feed(nome):
    if nome in session:
        return Response(utilizador.obtemUser(nome).transmite(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/login<string:nome>')
def login(nome):
    session[nome] = "Admin"
    print(nome)
    id = int(round(time.time() * 1000))
    u = utilizador.Utilizador(nome, id)
    utilizador.UTILIZADORES_ATIVOS.append(u)
    return "Ligou"


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=False)
