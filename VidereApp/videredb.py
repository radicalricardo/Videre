from sqlalchemy import create_engine, text, MetaData
import flask
import bcrypt
import time

# TODO: Inserir frames com execute many

engine = create_engine('postgresql+psycopg2://postgres:admin@localhost:5432/Videre', echo=False, future=True)

videreMETA = MetaData()
videreMETA.reflect(bind=engine)


# UTILIZADOR

def inserirUtilizador(username, password):
    hashedPW = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    statement = text(f"INSERT INTO utilizadores (username, password) VALUES ('{username}', '{hashedPW.decode()}')")
    with engine.connect() as con:
        con.execute(statement)
        con.commit()


def verificaUtilizador(username, password):
    with engine.connect() as con:
        result = con.execute(text(f"SELECT id, username, password "
                                  f"FROM utilizadores WHERE username = '{username}'")).fetchone()
        if result and bcrypt.checkpw(password.encode(), result[2].encode()):  # tb verifica se existe username
            return result[0]
        else:
            return None


# STREAM URLS

def inserirStream(user_id, stream_link , videre_url):
    with engine.connect() as con:
        con.execute(text(f"INSERT INTO stream_urls (user_id, stream_link, videre_url) "
                                  f"VALUES ({user_id}, '{stream_link}', '{videre_url}')"))
        con.commit()


def verificaCriador(user_id, videre_url):
    with engine.connect() as con:
        result = con.execute(text(f"SELECT user_id, videre_url FROM stream_urls "
                                  f"WHERE videre_url = '{videre_url}' AND user_id = '{user_id}'")).fetchone()
        if result:
            return True
        else:
            return False


def deleteStreamURL(videre_url):
    with engine.connect() as con:
        con.execute(text(f"DELETE FROM stream_urls WHERE videre_url = '{videre_url}'"))
        con.commit()


def buscaURLs(user_id):
    with engine.connect() as con:
        URLs = []
        result = con.execute(text(f"SELECT stream_link, videre_url FROM stream_urls WHERE user_id = {user_id}"))
        for row in result:
            URLs.append(row[1])
        return URLs


# FRAMES

def guardaFrame(frame, userid, timestamp, objects_found):
    """

    :type objects_found: [{"object_id": int, "confianca": double, "topLeft":[x,y], "bottomRight":[w,z]}, ... ]
    """
    frameName = f"{userid}-{time.strftime('%Y%m%d_%H%M%S', time.gmtime(timestamp))}"
    framePath = f"frames/{frameName}"
    newFrame = open(framePath + ".jpg", "x")
    newFrame.write(frame)
    with engine.connect() as con:
        frameID = con.execute(text(f"INSERT INTO frames (timestamp, user_id, frame_path) "
                                   f"VALUES ('{time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(timestamp))}', {userid}, '{frameName}') RETURNING id")).fetchone()
        con.commit()

        """
        videreMETA.tables["objects_found"].insert()
        con.execute(videreMETA.tables["objects_found"].insert(),
                    objects_found)
        con.commit()
        """
        for object in objects_found:
            topLeft = object.get("topLeft")
            bottomRight = object.get("bottomRight")
            stmt = "INSERT INTO objects_found VALUES (" + str(frameID[0]) + ", " + str(
                object.get("object_id")) + ", " + str(object.get("confianca")) + ", '{" + str(topLeft[0]) + ", " + str(
                topLeft[1]) + "}', '{" + str(bottomRight[0]) + ", " + str(bottomRight[1]) + "}')"
            # statement = text("INSERT INTO objects_found VALUES (%d, %d, %f, '{{%d, %d}}', '{{%d, %d}}')".format(frameID[0], object.get("object_id"), object.get("confianca"), topLeft[0],topLeft[1], bottomRight[0], bottomRight[1]))
            statement = text(stmt)
            con.execute(statement)
            con.commit()

# inserirUtilizador("FreeDom", "123")
