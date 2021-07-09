import os


# Port e flag de debug da aplicação
port = 5000
debugFlag = True

# Pastas
pastaFrames = "frames"
pastaVideos = "videos"

# Parametros do yolo
yoloPath = "yolo/yolov3.cfg"
yoloPathWeights = "yolo/yolov3.weights"
yoloDataset = "yolo/coco.names"

# basi di dados
database = 'postgresql+psycopg2://postgres:admin@localhost:5432/Videre'

# Sessão
chaveSession = os.urandom(24)
