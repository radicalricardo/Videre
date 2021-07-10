from app import app as VidereApp
import config

if __name__ == "__main__":
    config.pastas()
    VidereApp.run(port=config.port, debug=config.debugFlag)
