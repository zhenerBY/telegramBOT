from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, ForeignKey, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

from rates import Rates

HOST = 'ec2-34-197-135-44.compute-1.amazonaws.com'
USERNAME = 'emlftjtatnyzpt'
DATBASE = 'd5ps6u4quumv6b'
PORT = '5432'
PASSWORD = '0ff55cfd0fd0f6022a2e78e8b0692ee75345045a50a85b452b241c5c3b90d4a0'

engine = create_engine(f'postgresql+psycopg2://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATBASE}')

Base = declarative_base()

class UpdateDate(Base):
    __tablename__ = 'UpdateDate'
    id = Column(Integer, primary_key=True)
    date = Column(Date)

    def __init__(self, date=datetime.now().date()):
        self.date = date

    def __repr__(self):
        return "<User('%s')>" % (self.date)

Base.metadata.create_all(engine)
