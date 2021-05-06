from flask import Flask, g
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text, create_engine, MetaData, Table, Column, Integer, String, ForeignKey
from sqlalchemy.orm import Session, registry, relationship

engine = create_engine('postgresql+psycopg2://postgres:postgres@localhost:5432/Videre', echo=False, future=True)
'''
#Core

metadata = MetaData()
object_table = Table(
    "object",
    metadata,
    Column('id', Integer, primary_key=True),
    Column('nome_objecto', String)
)

utilizadores_table = Table(
    "utilizadores",
    metadata,
    Column('id', Integer, primary_key=True),
    Column('username', String, nullable=False),
    Column('password', String, nullable=False)
)

frames_table = Table(
    "frames",
    metadata,
    Column('id',Integer, primary_key=True),
    Column('frame', String),
    Column('timestamp', String),
    Column('user_id', ForeignKey('utilizadores.id'))
)

objects_found_table = Table(
    "objects_found",
    metadata,
    Column('frame_id', ForeignKey('frames.id'), primary_key=True),
    Column('object_id', ForeignKey('object.id'), primary_key=True),
    Column('coord_box', String)

)

#ORM

mapper_registry = registry()
Base = mapper_registry.generate_base()
class Object(Base):
    __tablename__ = 'object'

    id = Column(Integer, primary_key=True)
    nome_objecto = Column(String)

    def __repr__(self):
        return f"Address(id={self.id!r}, email_address={self.email_address!r})"


some_table = Table("object", metadata, autoload_with=engine)


#explicito com texto
statement = text("select * from object")
with Session(engine) as session:
    result = session.execute(statement)
    for row in result:
        print(row)

'''
#----//---- dummy coisas

#guarda info sobre a bd
metaDummy = MetaData()

#reflete as tabelas da bd para o python
metaDummy.reflect(bind=engine)

#dummy select
def dummySelect(tabela, colunas):
    if colunas == '*':
        stringColuna = '*'
    else:
        stringColuna = ', '.join(colunas)
    statement = text(f"SELECT {stringColuna} FROM {tabela}")
    with engine.connect() as conn:
        result = conn.execute(statement)
        for row in result:
            print(row)

def dummyInsert(tabela, values):
    stringValues = ', '.join(str(value) for value in values)
    print(stringValues)
    statement = text(f"INSERT INTO {tabela} VALUES ('{stringValues}')")
    with engine.connect() as conn:
        conn.execute(statement)
        conn.commit()


dummyInsert("object", ["mandioca"])
print("-//-")
dummySelect("object", "*")