import threading
import cv2
import numpy as np
import dataset

UTILIZADORES_ATIVOS = []


def obtemUser(nome):
    for i in UTILIZADORES_ATIVOS:
        if i.id == nome:
            return i


class Utilizador:
    def __init__(self, id_c, lnk):
        self.id = id_c
        self.imagem = cv2.VideoCapture(lnk)
        self.net = cv2.dnn.readNet("yolov3.cfg", "yolov3.weights")

        # Inicia CUDA, se utilizadoe não tiver, estas linhas são ignoradas
        self.net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
        self.net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)

    def __del__(self):
        self.imagem.release()

    def terminaProcesso(self):
        pass

    def criaProcesso(self):
        threading.Thread(target=self.transmite).start()

    def transmite(self):
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
            yield b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n'  # ????? mas funciona

            if cv2.waitKey(1) & 0xFF == ord('q'):  # Termina aplicação (é preciso carregar 50 vezes no Q porque sim)
                break
