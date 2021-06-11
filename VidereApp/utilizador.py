import random
import threading
import time
import uuid
import cv2
import numpy as np
import dataset
import config
import videredb
import app as main

UTILIZADORES_ATIVOS = {}  # Lista de mantem todos os utilizadores em processo no servidor


# Obtem dados do utilizador, usado para obter url da camara e thumbnail, obter objeto da camara e video
def obtemCrm(nome, vid):
    if nome in UTILIZADORES_ATIVOS and vid in UTILIZADORES_ATIVOS.get(nome).camaras:
        return UTILIZADORES_ATIVOS.get(nome).camaras.get(vid)


class Utilizador:
    def __init__(self, id_u):
        self.id = id_u
        self.camaras = {}

    def CriaCamara(self, lnk, nome, filtros):
        vid = str(uuid.uuid1()).replace("-", "")  # Gera o id do video que também é usado para url para aceder via web
        cmr = Camara(lnk, vid, self.id, nome, filtros)
        self.camaras[vid] = cmr
        threading.Thread(target=cmr.processa).start()

    def obtemCamarasLigacao(self):
        cmrs = {}
        for i in self.camaras:
            cmrs[self.camaras[i].nome] = i
        return cmrs


class Camara:
    def __init__(self, lnk, vid, id_user, c_nome, filtros):
        self.filtros = filtros
        self.nome = c_nome
        self.id = vid
        self.id_user = id_user
        self.imagem = cv2.VideoCapture(lnk, 0)
        self.net = cv2.dnn.readNet(config.yoloPath, config.yoloPathWeights)
        self.framecurrente = None
        self.tempoInicial = time.time()  # Tempo inicial da contagem para guardar a proxima frame da BD
        self.tempoPassado = 0

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

    def obtemThumbnail(self):
        if self.framecurrente is None:
            return None
        else:
            return b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + self.framecurrente + b'\r\n'

    def __del__(self):
        self.imagem.release()

    def processa(self):
        while True:
            ativo, frame = self.imagem.read()
            tamanho = frame.shape

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
                for ObjetoApanhado in p:
                    pontuacoes = ObjetoApanhado[5:]
                    class_id = np.argmax(pontuacoes)

                    if class_id not in self.filtros: # Este objeto detetado não está presente nos filtros para detetar
                        continue

                    certeza = pontuacoes[class_id]

                    if certeza > 0.5:
                        # Otem posição (eu não percebo a magia negra que o net.forward faz, mas as posições das coisas estão ai)
                        centroX = int(ObjetoApanhado[0] * comprimento)
                        centroY = int(ObjetoApanhado[1] * altura)
                        c = int(ObjetoApanhado[2] * comprimento)
                        a = int(ObjetoApanhado[3] * altura)
                        x = int(centroX - c / 2)
                        y = int(centroY - a / 2)

                        caixas.append([x, y, c, a])
                        confidences.append(float(certeza))
                        class_ids.append(class_id)

            indexes = cv2.dnn.NMSBoxes(caixas, confidences, 0.5, 0.4)

            objetos_captuados_frame = []
            for i in indexes:
                objeto_no_frame = {}
                i = i[0]
                caixa = caixas[i]
                x = caixa[0]
                y = caixa[1]
                w = caixa[2]
                h = caixa[3]
                objeto_no_frame["object_id"] = class_ids[i]
                objeto_no_frame["confianca"] = confidences[i]
                objeto_no_frame["topLeft"] = [x, y]
                objeto_no_frame["bottomRight"] = [w, h]
                objetos_captuados_frame.append(objeto_no_frame)
                label = str(dataset.classes[class_ids[i]])
                cor = dataset.classes_cores[class_ids[i]]
                cv2.rectangle(frame, (x, y), (x + w, y + h), cor, 2)

                # Impede que texto fique fora do ecrã
                if y < 40: # se o X estiver 40 pixeis perto do topo da imagem
                    y += 45 # Baixa 45 pixeis
                if x < 5: x += 5

                if x + (len(label)+5)*15 > tamanho[1]: # Impede que o texto saia para o lado da imagem
                    x -= (len(label)+5)*15

                # Faz um texto em baixo que serve como contorno
                cv2.putText(frame, label + " " + str(round(confidences[i], 2)), (x - 1, y - 10),
                            cv2.FONT_HERSHEY_DUPLEX, 1, (255, 255, 255), 2, lineType=cv2.LINE_AA)

                # Nome do objeto, texto de cima
                cv2.putText(frame, label + " " + str(round(confidences[i], 2)), (x, y - 10), cv2.FONT_HERSHEY_DUPLEX, 1,
                            cor, 1, lineType=cv2.LINE_AA)

            # Converte para jpg
            _, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            self.framecurrente = frame

            # Guarda a imagem na Base Dados
            if self.tempoPassado > 5:
                if len(indexes) > 0:
                    self.tempoInicial = time.time()
                    print(self.id)
                    videredb.guardaFrame(frame, self.id_user, time.time(), objetos_captuados_frame)
                    print("GRAVOU NA BD")
                self.tempoPassado = 0
            else:
                self.tempoPassado = time.time() - self.tempoInicial
