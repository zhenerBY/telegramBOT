from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, ForeignKey, Date, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

from datetime import datetime

from rates import Rates
from DBtestCURR import UpdateDate

HOST = 'ec2-34-197-135-44.compute-1.amazonaws.com'
USERNAME = 'emlftjtatnyzpt'
DATBASE = 'd5ps6u4quumv6b'
PORT = '5432'
PASSWORD = '0ff55cfd0fd0f6022a2e78e8b0692ee75345045a50a85b452b241c5c3b90d4a0'

engine = create_engine(f'postgresql+psycopg2://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATBASE}')

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


class RatesList(Base):
    __tablename__ = 'RatesList'
    id = Column(Integer, primary_key=True)
    cur_id = Column(Integer, ForeignKey('CurrenciesList.id'))
    cur_scale = Column(Integer)
    cur_rate = Column(Float)
    cur_date = Column(Date)
    сurrency = relationship('CurrenciesList', backref='rate')

    def __init__(self, cur_id, cur_scale, cur_rate, cur_date=datetime.now().date()):
        self.cur_id = cur_id
        self.cur_scale = cur_scale
        self.cur_rate = cur_rate
        self.cur_date = cur_date

    def __repr__(self):
        return "<User('%s', '%s', '%s', '%s')>" % (self.cur_id, self.cur_scale, self.cur_rate, self.cur_date)


Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()
updatedate = session.query(UpdateDate).first()
print(updatedate)
if updatedate.date == datetime.now().date() and session.query(CurrenciesList).first() is not None:
    print('Таблицу не меняеем')
else:
    print('Таблицу меняем')
    updatedate.date = datetime.now().date()
    currencies = session.query(CurrenciesList).all()
    for item in Rates.all_currencies_dictlist():
        # проверка на наличие записи в БД
        if len(list(filter(lambda x: x.cur_id == int(item['Cur_ID']), currencies))) == 0:
            session.add(CurrenciesList(item['Cur_ID'], item['Cur_Name'], item['Cur_Abbreviation']))
        else:
            currency = list(filter(lambda x: x.cur_id == int(item['Cur_ID']), currencies))[0]
            currency.cur_id = item['Cur_ID']
            currency.cur_name = item['Cur_Name']
            currency.cur_abbreviation = item['Cur_Abbreviation']
    session.commit()

    # это работает
    # a = session.query(CurrenciesList).filter(CurrenciesList.cur_name.ilike('%' + 'доллар' + '%')).all()
    # list(filter(lambda x:x.cur_id == 440, a))

firs = RatesList(397, 1, 2.5)
session.add(firs)
session.commit()