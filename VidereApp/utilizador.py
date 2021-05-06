import random
import threading
import uuid
import cv2
import numpy as np
import dataset

UTILIZADORES_ATIVOS = []  # Lista de mantem todos os utilizadores em processo no servidor (simula BD de momento)


# Uso de testes apenas, extremamente lento em uso de mundo real
def obtemUser(nome, vid):  # Função temporaria para obter um utilizador com camara em processo com id do video
    for i in UTILIZADORES_ATIVOS:
        if i.id == nome:
            for n in i.videos:
                if n.id == vid:
                    return n


class Utilizador:
    def __init__(self, id_u):
        self.id = id_u
        self.videos = []

    def iniciaVideo(self, lnk):
        vd = Camara(lnk)
        self.videos.append(vd)
        threading.Thread(target=vd.processa).start()
        # threading.Thread(target=corre).start()


class Camara:
    def __init__(self, lnk):
        self.id = str(uuid.uuid1()).replace("-", "")
        self.imagem = cv2.VideoCapture(0, lnk)
        self.net = cv2.dnn.readNet("yolo/yolov3.cfg", "yolo/yolov3.weights")
        self.framecurrente = None

        # Inicia CUDA, se utilizador não suportar, estas linhas são ignoradas
        if cv2.cuda.getCudaEnabledDeviceCount() > 0:
            self.net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
            self.net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)
        else:
            self.net.setPreferableBackend(cv2.dnn.DNN_BACKEND_DEFAULT)
            self.net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

    def terminaVideo(self):
        pass

    def obtemFrame(self):
        while True:
            yield b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + self.framecurrente + b'\r\n'

    def obtemTumbnail(self):
        if self.framecurrente is None:
            return None
        else:
            return b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + self.framecurrente + b'\r\n'

    def __del__(self):
        self.imagem.release()

    def processa(self):
        while True:
            ativo, frame = self.imagem.read()
            if not ativo: break

            layer_names = self.net.getLayerNames()
            outputlayers = [layer_names[i[0] - 1] for i in self.net.getUnconnectedOutLayers()]

            altura = frame.shape[0]
            comprimento = frame.shape[1]
            blob = cv2.dnn.blobFromImage(frame, 1 / 255, (128, 128), [0, 0, 0], True, crop=False)
            self.net.setInput(blob)
            processados = self.net.forward(outputlayers)

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
                label = str(dataset.classes[class_ids[i]])
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(frame, label + " " + str(round(confidences[i], 2)), (x, y - 10), cv2.FONT_HERSHEY_DUPLEX, 1,
                            (0, 0, 0), 2)

            # Converte para jpg
            _, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            self.framecurrente = frame
