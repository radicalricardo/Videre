import config
from sqlalchemy import create_engine, text

engine = create_engine(config.database, echo=False, future=True)
names = open("../BaseDados/coco.names", "r")
with engine.connect() as con:
    for i in names:
        i = i[:-1]
        statement = text(f"INSERT INTO OBJECT (nome_objecto) VALUES ('{i}')")
        con.execute(statement)
    con.commit()
    '''
    result = con.execute(text("SELECT * FROM OBJECT"))
    for row in result:
        print(row)
    '''

    # para dar reset aos ids da tabela (que devem ser de 0 a 79) fazer a query TRUNCATE TABLE OBJECT RESTART IDENTITY CASCADE
