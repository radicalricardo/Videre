import config

classes = {}  # Classes de nomes dos objetos
with open(config.yoloDataset, "r") as f:  # Coco dataset é o dataset do yolo que contem os mais de 80 objetos
    # classes = [line.strip() for line in f.readlines()]    # de quando o classes era uma classe

    counter = 0
    for i in f:
        classes[counter+1] = i.strip()
        counter+=1

    classes = dict(sorted(classes.items(), key=lambda item:item[1]))