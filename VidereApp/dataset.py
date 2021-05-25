import config

classes = []  # Classes de noms dos objetos
with open(config.yoloDataset, "r") as f:  # Coco dataset é o dataset do yolo que contem os mais de 80 objetos
    classes = [line.strip() for line in f.readlines()]
