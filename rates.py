import requests

class Rates():
    HOST_CURRENCIES = 'https://www.nbrb.by/api/exrates/currencies/'
    HOST_RATES = 'https://www.nbrb.by/api/exrates/rates/'

    def __init__(self, cur:str):
        if Rates.check(cur):
            data = requests.get(Rates.HOST_RATES+cur, params={'parammode':2})
            json_data = data.json()
            # print(json_data)
            self.cur_abb = json_data['Cur_Abbreviation']
            self.cur_name = json_data['Cur_Name']
            self.rate = json_data['Cur_OfficialRate']
            self.date = json_data['Date']

    @classmethod
    def check(cls, cur:str) -> bool:
        if requests.get(cls.HOST_RATES+cur, params={'parammode':2}).status_code == 200:
            return True
        else:
            return False

    def text(self):
        text = 'Аббревиатура: ' + self.cur_abb + '\n'
        text += 'Название : ' + self.cur_name+ '\n'
        text += 'Дата : ' + self.date + '\n'
        text += 'Курс к бел. рублю : ' + str(self.rate)
        return text