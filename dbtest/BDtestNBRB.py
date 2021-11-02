from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from rates import Rates

HOST = 'ec2-34-197-135-44.compute-1.amazonaws.com'
USERNAME = 'emlftjtatnyzpt'
DATBASE = 'd5ps6u4quumv6b'
PORT = '5432'
PASSWORD = '0ff55cfd0fd0f6022a2e78e8b0692ee75345045a50a85b452b241c5c3b90d4a0'

engine = create_engine(f'postgresql+psycopg2://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATBASE}')

# def create_bases():

Base = declarative_base()

class CurrenciesList(Base):
    __tablename__ = 'CurrenciesList'
    id = Column(Integer, primary_key=True)
    cur_id = Column(Integer)
    cur_name = Column(String(200))
    cur_abbreviation = Column(String(5))

    def __init__(self, cur_id, cur_name, cur_abbreviation):
        self.cur_id = cur_id
        self.cur_name = cur_name
        self.cur_abbreviation = cur_abbreviation

    def __repr__(self):
        return "<User('%s','%s', '%s')>" % (self.cur_id, self.cur_name, self.cur_abbreviation)

Base.metadata.create_all(engine)

# def fill_bases():

Session = sessionmaker(bind=engine)
session = Session()
for item in Rates.all_currencies_dictlist():
    session.add(CurrenciesList(item['Cur_ID'], item['Cur_Name'], item['Cur_Abbreviation']))

session.commit()