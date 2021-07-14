import config

classes = {}  # Classes de nomes dos objetos (id, nome)
classes_cores = {}
cores = [(255, 0, 0), (255, 163, 0), (255, 39, 220), (0, 39, 220), (0, 248, 85), (109, 51, 64), (253, 250, 247), (1, 142, 41)]

with open(config.yoloDataset, "r", encoding="utf-8") as f:  # Coco dataset é o dataset do yolo que contem os 80 objetos
    apontador_cor = -1
    for c, i in enumerate(f):
        classes[c] = i.strip()
        if c % 10 == 0:  # A cada 10 objetos mete uma cor diferente (8 cores por 80 objetos)
            apontador_cor += 1
        classes_cores[c] = cores[apontador_cor]
    classes = dict(sorted(classes.items(), key=lambda item: item[1]))

