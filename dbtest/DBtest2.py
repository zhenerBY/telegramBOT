from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

HOST = 'ec2-34-197-135-44.compute-1.amazonaws.com'
USERNAME = 'emlftjtatnyzpt'
DATBASE = 'd5ps6u4quumv6b'
PORT = '5432'
PASSWORD = '0ff55cfd0fd0f6022a2e78e8b0692ee75345045a50a85b452b241c5c3b90d4a0'

engine = create_engine(f'postgresql+psycopg2://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATBASE}')

# metadata = MetaData()
# users_table = Table('users', metadata,
#     Column('id', Integer, primary_key=True),
#     Column('name', String(200)),
#     Column('fullname', String(200)),
#     Column('password', String(200))
# )
# metadata.create_all()

# engine.connect()


Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(200))
    fullname = Column(String(200))
    password = Column(String(200))

    def __init__(self, name, fullname, password):
        self.name = name
        self.fullname = fullname
        self.password = password

    def __repr__(self):
        return "<User('%s','%s', '%s')>" % (self.name, self.fullname, self.password)

class User2(Base):
    __tablename__ = 'users2'
    id = Column(Integer, primary_key=True)
    name = Column(String(200))
    fullname = Column(String(200))
    fullname2 = Column(String(200))
    password = Column(String(200))

    def __init__(self, name, fullname, password):
        self.name = name
        self.fullname = fullname
        self.password = password

    def __repr__(self):
        return "<User('%s','%s', '%s')>" % (self.name, self.fullname, self.password)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()