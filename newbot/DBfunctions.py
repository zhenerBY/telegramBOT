from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, ForeignKey, Date, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime

from DB import CurrenciesList, RatesList, UpdateDate
from DB import engine

from rates import Rates

Session = sessionmaker(bind=engine)
session = Session()


def db_currencieslist_upp():
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


def db_currencies_list() -> list:
    table = session.query(CurrenciesList).all()
    currencies_list = []
    for item in table:
        currencies_list.append([item.cur_name, item.cur_abbreviation])
    return sorted(currencies_list)


def db_text(abbreviation: str) -> str:
    # currency = session.query(RatesList).filter(RatesList.сurrency.cur_abbreviation == abbreviation).first()
    responce = session.query(CurrenciesList, RatesList).join(RatesList).filter(
        CurrenciesList.cur_abbreviation == abbreviation).filter(RatesList.cur_date == datetime.now().date()).all()
    currency = responce[0][0]
    rate = responce[0][1]
    text = 'Аббревиатура: ' + currency.cur_abbreviation + '\n'
    text += str(rate.cur_scale) + ' ' + currency.cur_name + ' = ' + str(rate.cur_rate) + ' BYN' + '\n'
    text += 'Дата : ' + rate.cur_date.isoformat()
    return text
    # return currency


def db_add_rate(abbreviation: str) -> None:
    db_currencieslist_upp()
    if Rates.check(abbreviation):
        curr = Rates(abbreviation)
        responce = session.query(CurrenciesList).filter(CurrenciesList.cur_abbreviation == abbreviation).all()[0]
        record = RatesList(responce.id, curr.scale, curr.rate)
        session.add(record)
        session.commit()
    else:
        print('Курс не найден. Добавление невозможно.')