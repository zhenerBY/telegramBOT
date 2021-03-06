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
    if updatedate.date == datetime.now().date() and session.query(CurrenciesList).first() is not None:
        pass
        # print('Таблицу не меняеем')
    else:
        # print('Таблицу меняем')
        print('Запрос в API списка всех валют')
        updatedate.date = datetime.now().date()
        currencies = session.query(CurrenciesList).all()
        for item in Rates.all_currencies_dictlist():
            # проверка на наличие записи в БД
            if len(list(filter(lambda x: x.cur_id == int(item['Cur_ID']), currencies))) == 0:
                session.add(
                    CurrenciesList(item['Cur_ID'], item['Cur_Name'], item['Cur_Names'], item['Cur_Abbreviation']))
            else:
                currency = list(filter(lambda x: x.cur_id == int(item['Cur_ID']), currencies))[0]
                currency.cur_id = item['Cur_ID']
                currency.cur_name = item['Cur_Name']
                currency.cur_names = item['Cur_Names']
                currency.cur_abbreviation = item['Cur_Abbreviation']
        session.commit()


def db_currencies_list() -> list:
    db_currencieslist_upp()
    table = session.query(CurrenciesList).all()
    currencies_list = []
    for item in table:
        currencies_list.append([item.cur_name, item.cur_abbreviation])
    return sorted(currencies_list)


def db_all_currencies_abblist() -> list:
    currencies_list = []
    for item in db_currencies_list():
        currencies_list.append(item[1])
    return sorted(currencies_list)


def db_text(abbreviation: str) -> str:
    db_currencieslist_upp()
    # проверка на существование записи
    if session.query(CurrenciesList, RatesList).join(RatesList).filter(
            CurrenciesList.cur_abbreviation == abbreviation).filter(
        RatesList.cur_date == datetime.now().date()).first() is None:
        print('Запрашиваем курсы из API')
        if Rates.check(abbreviation):
            db_add_rate(abbreviation)
        else:
            return 'Отсутсвует связь с API nbrb.by'
    else:
        print('Запрашиваем курсы из БД')
    responce = session.query(CurrenciesList, RatesList).join(RatesList).filter(
        CurrenciesList.cur_abbreviation == abbreviation).filter(RatesList.cur_date == datetime.now().date()).all()
    currency = responce[0][0]
    rate = responce[0][1]
    text = 'Аббревиатура: ' + currency.cur_abbreviation + '\n'
    text += str(rate.cur_scale) + ' ' + currency.cur_names + ' = ' + str(rate.cur_rate) + ' BYN' + '\n'
    text += 'Дата : ' + rate.cur_date.isoformat()
    return text


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


def db_check(abbreviation: str) -> bool:
    if abbreviation in db_all_currencies_abblist():
        return True
    else:
        return False
