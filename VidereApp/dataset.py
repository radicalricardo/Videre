import random

import config


classes = {}  # Classes de nomes dos objetos (id, nome)
classes_cores = {}
with open(config.yoloDataset, "r") as f:  # Coco dataset é o dataset do yolo que contem os mais de 80 objetos
    for c, i in enumerate(f):
        classes[c] = i.strip()
        classes_cores[c] = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        print(classes_cores[c])
    classes = dict(sorted(classes.items(), key=lambda item: item[1]))






