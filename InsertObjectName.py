
from sqlalchemy import create_engine, text

engine = create_engine('postgresql+psycopg2://postgres:postgres@localhost:5432/Videre', echo=False, future=True)
names = open("VidereApp/yolo/coco.names", "r")
with engine.connect() as con:
    for i in names:
        statement = text(f"INSERT INTO OBJECT (nome_objecto) VALUES ('{i}')")
        con.execute(statement)
    con.commit()
    '''
    result = con.execute(text("SELECT * FROM OBJECT"))
    for row in result:
        print(row)
    '''