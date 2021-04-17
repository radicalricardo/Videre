import time
from flask import Flask, render_template, Response
import cv2
import numpy as np

app = Flask(__name__)
imagem = cv2.VideoCapture(0)

# Prepara Yolo
# net = cv2.dnn.readNet("yolov3.cfg", "yolov3.weights")
net = cv2.dnn.readNet("yolov3-tiny.weights", "yolov3-tiny.cfg")  # tiny yolo
classes = []  # Classes de noms dos objetos
with open("coco.names", "r") as f:  # Coco dataset é o dataset do yolo que contem os mais de 40 objetos
    classes = [line.strip() for line in f.readlines()]
layer_names = net.getLayerNames()
outputlayers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]


def obtemFrames():
    while True:
        ativo, frame = imagem.read()
        if not ativo: break

        altura = frame.shape[0]
        comprimento = frame.shape[1]
        blob = cv2.dnn.blobFromImage(frame, 1 / 255, (128, 128), [0, 0, 0], True, crop=False)
        net.setInput(blob)
        processados = net.forward(outputlayers)

        class_ids = []
        confidences = []  # Grau de confiança sobre a imagem
        caixas = []
        for p in processados:
            for ObjetosApanhados in p:
                pontuacoes = ObjetosApanhados[5:]
                class_id = np.argmax(pontuacoes)
                certeza = pontuacoes[class_id]

                if certeza > 0.5:
                    # Otem posição (eu não percebo a magia negra que o net.forward faz, mas as posições das coisas estão ai)
                    centroX = int(ObjetosApanhados[0] * comprimento)
                    centroY = int(ObjetosApanhados[1] * altura)
                    c = int(ObjetosApanhados[2] * comprimento)
                    a = int(ObjetosApanhados[3] * altura)
                    x = int(centroX - c / 2)
                    y = int(centroY - a / 2)

                    caixas.append([x, y, c, a])
                    confidences.append(float(certeza))
                    class_ids.append(class_id)

        indexes = cv2.dnn.NMSBoxes(caixas, confidences, 0.5, 0.4)

        for i in indexes:
            i = i[0]
            caixa = caixas[i]
            x = caixa[0]
            y = caixa[1]
            w = caixa[2]
            h = caixa[3]
            label = str(classes[class_ids[i]])
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, label + " " + str(round(confidences[i], 2)), (x, y - 10), cv2.FONT_HERSHEY_DUPLEX, 1,
                        (0, 0, 0), 2)

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
    app.run(debug=False)
