import requests


class Rates():
    HOST_CURRENCIES = 'https://www.nbrb.by/api/exrates/currencies/'
    HOST_RATES = 'https://www.nbrb.by/api/exrates/rates/'

    def __init__(self, cur: str):
        if Rates.check(cur):
            data = requests.get(Rates.HOST_RATES + cur, params={'parammode': 2})
            json_data = data.json()
            # print(json_data)
            self.cur_id = json_data['Cur_ID']
            self.cur_abb = json_data['Cur_Abbreviation']
            self.cur_name = json_data['Cur_Name']
            self.rate = json_data['Cur_OfficialRate']
            self.date = json_data['Date']
            self.scale = json_data['Cur_Scale']

    @classmethod
    def check(cls, cur: str) -> bool:
        if requests.get(cls.HOST_RATES + cur, params={'parammode': 2}).status_code == 200:
            return True
        else:
            return False

    @classmethod
    def all_currencies(cls) -> str:
        listcurr = Rates.all_currencies_list()
        textlistcurr = ''
        for item in listcurr:
            textlistcurr += item[0] + ' - ' + item[1] + '\n'
        return textlistcurr

    @classmethod
    def all_currencies_list(cls) -> list:
        paramslist = [{'periodicity': '0'}, {'periodicity': '1'}]
        listcurr = []
        for params in paramslist:
            if requests.get(cls.HOST_RATES, params=params).status_code == 200:
                response = requests.get(cls.HOST_RATES, params=params)
                json_response = response.json()
                responsename = requests.get(cls.HOST_CURRENCIES)
                json_responsename = responsename.json()
                for item in json_response:
                    for item2 in json_responsename:
                        if item['Cur_ID'] == item2['Cur_ID']:
                            listcurr.append([item2['Cur_Name'], item2['Cur_Abbreviation']])
        return sorted(listcurr)


    def text(self):
        text = 'Аббревиатура: ' + self.cur_abb + '\n'
        text += str(self.scale) + ' ' + self.cur_name + ' = ' + str(self.rate) + ' BYN'  + '\n'
        text += 'Дата : ' + self.date
        return text
