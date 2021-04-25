import cv2

lista = []


def obtemUser(nome):
    for i in lista:
        if i.id == nome:
            return i


class Utilizador:
    def __init__(self, id):
        self.id = id
        self.camara = cv2.VideoCapture(0)
