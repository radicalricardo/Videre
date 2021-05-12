from sqlalchemy import create_engine, text
import flask
import bcrypt

engine = create_engine('postgresql+psycopg2://postgres:postgres@localhost:5432/Videre', echo=False, future=True)


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


#inserirUtilizador("DM","1234")
print(verificaUtilizador("DMSM", "1234"))