from sqlalchemy import create_engine, text
import flask
import bcrypt
import time

engine = create_engine('postgresql+psycopg2://postgres:postgres@localhost:5432/Videre', echo=False, future=True)


# UTILIZADOR

def inserirUtilizador(username, password):
    hashedPW = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    statement = text(f"INSERT INTO utilizadores (username, password) VALUES ('{username}', '{hashedPW.decode()}')")
    with engine.connect() as con:
        con.execute(statement)
        con.commit()


def verificaUtilizador(username, password):
    with engine.connect() as con:
        result = con.execute(text(f"SELECT username, password "
                                  f"FROM utilizadores WHERE username = '{username}'")).fetchone()
        if result != None and bcrypt.checkpw(password.encode(), result[1].encode()):    # tb verifica se existe username
            return True
        else:
            return False


# FRAMES


def guardaFrame(frame, userid, timestamp):
    frameName = f"{userid}-{time.strftime('%Y%m%d_%H%M%S', time.gmtime(timestamp))}"
    framePath = f"frames/{frameName}"
    newFrame = open(framePath + ".jpg", "x")
    newFrame.write(frame)
    with engine.connect() as con:
        con.execute(text(f"INSERT INTO frames (timestamp, user_id, frame_path) "
                         f"VALUES ('{time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(timestamp))}', {userid}, '{frameName}')"))
        con.commit()


# OBJECT_FOUND


def guardaObjectos(frameid, objectid, caixa: list, confianca):      # tenho de pensar se fica incluido no #frames ou não
    pass


