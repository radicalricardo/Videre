
from sqlalchemy import create_engine, text

engine = create_engine('postgresql://postgres:admin@localhost:5432/Videre', echo=False, future=True)
names = open("coco.names", "r")
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

    #para dar reset ao indicador fazer a query TRUNCATE TABLE OBJECT RESTART IDENTITY CASCADE
