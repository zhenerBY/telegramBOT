import requests
from rates import Rates

class Bot:
    telegram_api_url = f"https://api.telegram.org/bot"

    def __init__(self, token):
        self.token = token
        self.url = f'{self.telegram_api_url}{self.token}'
        self.last_update_id = None


    def get_updates(self):
        params = {'offset':90}
        req = requests.get(f'{self.url}/getUpdates', params=params)
        json_data = req.json()
        if not json_data['ok']:
            return {"error": json_data['description']}
        return json_data['result']


    def get_last_update(self):
        updates = self.get_updates()
        if 'error' in updates:
            return updates
        last_update = updates[-1] if updates else None
        if last_update and last_update['update_id'] != self.last_update_id:
            self.last_update_id = last_update['update_id']
        else:
            last_update = None
        return last_update

    def get_message(self):
        last_update = self.get_last_update()
        print(last_update)
        if last_update is None:
            return None
        if 'error' in last_update:
            raise ValueError('Non valid update')
        chat_id = last_update[list(last_update.keys())[1]]['chat']['id'] #выше нельзя. Надо возвращать None
        if 'message' not in last_update.keys(): #проверка на Тип
            return None
        elif 'sticker' in last_update['message'].keys():
            text = 'Смайл стекера : ' + last_update['message']['sticker']['emoji']
        else:
            try:
                text = last_update['message']['text']
            except KeyError:
                return None
        if '/help' in text:
            param = text.split(' ', maxsplit=1)[1].strip() if len(text.split()) > 1 else None
            text = f'Мы были рады Вам помочь! Параметр - "{param}"'
        if '/curr' in text:
            param = text.split(' ', maxsplit=1)[1].strip() if len(text.split()) > 1 else None
            if param:
                if Rates.check(param):
                    curr = Rates(param)
                    text = curr.text()
                else:
                    text =f'Курса для валюты "{param}" на NBRB.BY нет.'
            else:
                text = 'Укажите запрос в виде "/curr EUR")'
        return {"chat_id": chat_id, "text": text}

    def send_message(self, chat_id, text):
        text = text
        params = {'chat_id':chat_id, 'text':text}
        req = requests.get(url=self.url+'/sendMessage', params=params)
        print(text)
        print(req)
        if not req.json()['ok']:
            return {"error": req['description']}
        return req.json()