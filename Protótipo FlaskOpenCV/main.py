import time

from flask import Flask, render_template, Response
import cv2

app = Flask(__name__)
if os.environ.get('WERKZEUG_RUN_MAIN') or Flask.debug is False:
    imagem = cv2.VideoCapture(-1)

carasDados = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

antigo_frame = 0
novo_frame = 0


def obtemFrames():
    global antigo_frame
    global novo_frame

    while True:
        _, frame = imagem.read()

        # Framerate
        novo_frame = time.time()
        fps = int(1 / (novo_frame - antigo_frame))
        antigo_frame = novo_frame
        frame = cv2.putText(frame, str(fps), (0, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1, cv2.LINE_AA)

        cinza = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # IA tem maior facilidade a detetar coisas se não tiver cores
        caras = carasDados.detectMultiScale(cinza, scaleFactor=1.3, minNeighbors=5, minSize=(30, 30))

        for (x, y, w, h) in caras:  # Desenha quadrados verdes á volta da cara
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            frame = cv2.putText(frame, ':D', (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1, cv2.LINE_AA)

        # Converte para jpg para funcionar
        _, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n'  # ????? mas funciona


@app.route('/video_feed')
def video_feed():
    return Response(obtemFrames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)
