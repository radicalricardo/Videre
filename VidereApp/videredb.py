import cv2
import numpy
from sqlalchemy import create_engine, text, MetaData
import flask
import config
import bcrypt
import time
import os

# TODO: Inserir frames com execute many
import dataset

engine = create_engine(config.database, echo=False, future=True)

videreMETA = MetaData()
videreMETA.reflect(bind=engine)


# CRUD

def selectTabela(tabela):
    with engine.connect() as con:
        return con.execute(text(f"SELECT * FROM {tabela}"))


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


def verificaDisponibilidadeUser(user):
    with engine.connect() as con:
        result = con.execute(text(f"SELECT username "
                                  f"FROM utilizadores WHERE username = '{user}'")).fetchone()
        if not result:
            return True
        else:
            return False


# STREAM URLS

def inserirStream(user_id, videre_url):
    with engine.connect() as con:
        con.execute(text(f"INSERT INTO stream_urls (user_id, videre_url) "
                         f"VALUES ({user_id}, '{videre_url}')"))
        con.commit()


def verificaCriador(user_id, videre_url):
    with engine.connect() as con:
        result = con.execute(text(f"SELECT user_id, videre_url FROM stream_urls "
                                  f"WHERE videre_url = '{videre_url}' AND user_id = '{user_id}'")).fetchone()
        if result:
            return True
        else:
            return False


def deleteStreamURL(videre_url, user_id):
    with engine.connect() as con:
        con.execute(text(
            f"DELETE FROM stream_urls WHERE videre_url = '{videre_url}' and user_id = {user_id} RETURNING *")).fetchone()
        con.commit()


def apagaTabelaStreams():
    with engine.connect() as con:
        con.execute(text(f"DELETE FROM stream_urls"))
        con.commit()


# FRAMES

def guardaFrame(frame, userid, timestamp, objects_found):
    """
    :type userid: int # id do utilizador na base de dados
    :type objects_found: [{"object_id": int, "confianca": double, "topLeft":[x,y], "bottomRight":[w,z]}, ... ]
    """
    nomeFrame = f"{userid}-{time.strftime('%Y%m%d_%H%M%S', time.gmtime(timestamp))}"
    caminhoFrame = f"{config.pastaFrames}/{nomeFrame}.png"
    img = cv2.imdecode(numpy.fromstring(frame, numpy.uint8), cv2.IMREAD_UNCHANGED)
    cv2.imwrite(caminhoFrame, img)

    with engine.connect() as con:
        frameID = con.execute(text(f"INSERT INTO frames (timestamp, user_id, frame_path) "
                                   f"VALUES ('{time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(timestamp))}', {userid}, '{nomeFrame}') RETURNING id")).fetchone()
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


def obtemFrames(user_id):
    with engine.connect() as con:
        objetos = con.execute(text(
            f"SELECT object_id, frame_path "
            f"FROM frames inner join objects_found on frames.id = objects_found.frame_id "
            f"where user_id = {user_id}"))
        if objetos:
            fotos = {}
            for row in objetos:
                if row[1] in fotos:
                    if dataset.classes[row[0]] in fotos[row[1]]: continue
                    fotos[row[1]].append(dataset.classes[row[0]])
                else:
                    fotos[row[1]] = []
                    fotos[row[1]].append(dataset.classes[row[0]])

            for i in fotos:
                fotos[i] = " ".join(str(v) for v in fotos[i])
            return fotos
        else:
            return None


def obtemDadaFrame(user_id, frame):
    with engine.connect() as con:
        data = con.execute(text(
            f"SELECT timestamp "
            f"FROM frames "
            f"where user_id = {user_id} and frame_path= '{frame}'"))
        if data:
            dataframe = ""
            for i in data:
                dataframe = i[0]

            return str(dataframe) + " UTC"
        else:
            return None


def removeFrame(frame, user_id):
    with engine.connect() as con:
        result = con.execute(
            text(f"DELETE FROM frames WHERE frame_path = '{frame}' and user_id = {user_id} RETURNING *")).fetchone()
        if not result:
            return False
        path = f"{config.pastaFrames}/{frame}.png"
        if os.path.exists(path):
            os.remove(path)
        else:
            return False
        con.commit()
    return True


def seUserDonoFrame(frame, user_id):
    with engine.connect() as con:
        result = con.execute(
            text(f"SELECT * FROM frames WHERE frame_path = '{frame}' and user_id = {user_id}")).fetchone()
        if not result:
            return False
        else:
            return True


# VIDEOS

def guardaVideo(nomeVideo, userid, objects_found):
    """
    :type userid: int # id do utilizador na base de dados
    :type objects_found: lista com os n??meros dos objectos detetados
    """

    with engine.connect() as con:
        videoID = con.execute(text(f"INSERT INTO videos (timestamp, user_id, frame_path) "
                                   f"VALUES ('{time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time.time()))}', {userid}, "
                                   f"'{nomeVideo}') RETURNING id")).fetchone()
        con.commit()

        for object in objects_found:
            statement = text(f"INSERT INTO objects_video VALUES ({videoID[0]}, {object})")
            con.execute(statement)
            con.commit()


def obtemVideo(user_id):
    with engine.connect() as con:
        objetos = con.execute(text(
            f"SELECT frame_path, object_id, timestamp "
            f"FROM videos inner join objects_video on videos.id = objects_video.video_id "
            f"where user_id = {user_id}"))

        videos_user = {}
        for row in objetos:
            if row[0] in videos_user:
                if dataset.classes[row[1]] in videos_user[row[0]]: continue
                videos_user[row[0]].append(dataset.classes[row[1]])
            else:
                videos_user[row[0]] = []
                videos_user[row[0]].append(dataset.classes[row[1]])

        for i in videos_user:
            videos_user[i] = " ".join(str(v) for v in videos_user[i])

        return videos_user


def removeVideo(video, user_id):
    with engine.connect() as con:
        result = con.execute(
            text(f"DELETE FROM videos WHERE frame_path = '{video}' and user_id = {user_id} RETURNING *")).fetchone()
        if not result:
            return False
        path = f"{config.pastaVideos}/{video}.webm"
        if os.path.exists(path):
            os.remove(path)
        else:
            return False
        con.commit()
    return True


def seUserDonoVideo(frame, user_id):
    with engine.connect() as con:
        result = con.execute(
            text(f"SELECT * FROM videos WHERE frame_path = '{frame}' and user_id = {user_id}")).fetchone()
        if not result:
            return False
        else:
            return True
