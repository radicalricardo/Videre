import config

classes = {}  # Classes de nomes dos objetos (id, nome)
with open(config.yoloDataset, "r") as f:  # Coco dataset é o dataset do yolo que contem os mais de 80 objetos
    for c, i in enumerate(f):
        classes[c] = i.strip()
    classes = dict(sorted(classes.items(), key=lambda item: item[1]))

