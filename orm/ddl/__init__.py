

import os
import random
import sqlalchemy
import sqlalchemy.orm
from faker import Faker
from dotenv import load_dotenv
from geoalchemy2 import Geometry
load_dotenv()
from .dml import User

db_params = sqlalchemy.URL.create(
    drivername='postgresql+psycopg2',
    username=os.getenv("POSTGRES_USER"),
    password=os.getenv("POSTGRES_PASSWORD"),
    host=os.getenv("POSTGRES_HOST"),
    database=os.getenv("POSTGRES_DB"),
    port=os.getenv("POSTGRES_PORT")

)

engine = sqlalchemy.create_engine(db_params)
connection = engine.connect()

Base = sqlalchemy.orm.declarative_base()

class User(Base):
    __tablename__ = 'main_table'

    id = sqlalchemy.Column(sqlalchemy.Integer(), primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String(100), nullable=True)
    location = sqlalchemy.Column('geom', Geometry(geometry_type='POINT', srid=4326), nullable=True)

Base.metadata.create_all(engine)

Session = sqlalchemy.orm.sessionmaker(bind=engine)
session = Session()

#lista_userow: list = []
#fake = Faker()

# for item in range(10_000):
#    lista_userow.append(
#        User(
#            name=fake.name(),
#            location=f'POINT({random.uniform(14,24)} {random.uniform(49,55)})'
#        )
#     )

#users_from_db = session.query(User).all()

user_from_db = session.query(User).all()

for user in user_from_db:
    if user.name == 'Maria Carey':
        user.query.delete()
    print(user.name)

# for user in users_from_db:
#     print(user.name)


# session.add_all(lista_userow)
session.commit()

session.flush()
connection.close()
engine.dispose()

def main():

if __name__== __main__:
    main()