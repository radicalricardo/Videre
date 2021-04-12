import cv2
import numpy as np
import time

# Comenta e descomenta o dataset desejado
# net = cv2.dnn.readNet("yolov3-tiny.weights", "yolov3-tiny.cfg")  # Melhor Performance, Pior resultado
net = cv2.dnn.readNet("yolov3.cfg", "yolov3.weights") # Pior Performance, Melhor resultado

# https://pjreddie.com/media/files/yolov3-spp.weights site oficial do ficheiro do yolov3.weights

classes = []  # Classes de noms dos objetos
with open("coco.names", "r") as f:  # Coco dataset é o dataset do yolo que contem os mais de 40 objetos
    classes = [line.strip() for line in f.readlines()]

# Cenas que não de deve mexer
layer_names = net.getLayerNames()
outputlayers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]

# Cor das caixas
CoresCaixas = np.random.uniform(0, 255, size=(len(classes), 3)) # faz uma cor aletaorio para cada objeto
imagem = cv2.VideoCapture(0)  # Obtem imagem webcam
font = cv2.FONT_HERSHEY_PLAIN

# Util para determinar framerate
tempo_inicial = time.time()
frame_id = 0

while True:
    ativo, frame = imagem.read()  # Capta imagem OpenCV
    if ativo: # Se for falso é porque deixou de receber imagem
        break
    frame_id += 1
    altura = frame.shape[0]
    comprimento = frame.shape[1]

    blob = cv2.dnn.blobFromImage(frame, 1/255, (320, 320), [0, 0, 0], True, crop=False)  # cria blob da imagem
    # 320x320 com Yolo normal, 1~2 fps (Fica possivel detetar objetos pelo menos dentro de 3 metros)
    # 128x128 com Yolo Normal a 5~6 fps (Menos de 1 metro)
    # 68x68 com Yolo Normal a 15 fps (Objetos a mais de 15 centimetos pode ser muito dificil de detetar
    # Redução da resolução tem claro aumento desempenho, no Yolo Tiny a superior a 30fps a 128x128
    # Resultados com i5-8300H a 4.0 GHz, prolongamento de tempo verificou-se a 40 Watts

    net.setInput(blob)
    processados = net.forward(outputlayers)

    class_ids = []
    confidences = [] # Grau de confiança sobre a imagem
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
        cv2.rectangle(frame, (x, y), (x + w, y + h), CoresCaixas[class_ids[i]], 2)
        cv2.putText(frame, label + " " + str(round(confidences[i], 2)), (x, y + 30), font, 1, (0, 0, 0), 2)

    # FrameRate
    tempo_passado = time.time() - tempo_inicial
    cv2.putText(frame, "FPS:" + str(round(frame_id / tempo_passado, 2)), (10, 50), font, 2, (0, 0, 0), 1)
    cv2.imshow("JANELA", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):  # Termina aplicação (é preciso carregar 50 vezes no Q porque sim)
        break

imagem.release()
cv2.destroyAllWindows()
