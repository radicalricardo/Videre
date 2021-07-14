import videredb
from app import app as VidereApp
import config

if __name__ == "__main__":
    config.pastas()
    videredb.apagaTabelaStreams() # Remove todos os dados em relações ás streams sempre que o servidor inicia
    VidereApp.run(port=config.port, debug=config.debugFlag)
