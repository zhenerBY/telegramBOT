import requests
from rates import Rates
import json

class Bot:
    telegram_api_url = f"https://api.telegram.org/bot"

    def __init__(self, token):
        self.token = token
        self.url = f'{self.telegram_api_url}{self.token}'
        self.last_update_id = None


    def get_updates(self):
        params = {'offset':-90}
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

    def get_message(self, last_update):
        last_update = last_update
        print(last_update)
        if 'error' in last_update:
            raise ValueError('Non valid update')
        elif 'sticker' in last_update['message'].keys():
            text = 'Смайл стекера : ' + last_update['message']['sticker']['emoji']
        else:
            try:
                text = last_update['message']['text']
            except KeyError:
                return None
        chat_id = last_update[list(last_update.keys())[1]]['chat']['id']  # выше нельзя. Надо возвращать No
        if '/help' == text[:5]:
            param = text.split(' ', maxsplit=1)[1].strip() if len(text.split()) > 1 else None
            text = f'Мы были рады Вам помочь! Параметр - "{param}"'
        elif '/curr' == text[:5]:
            param = text.split(' ', maxsplit=1)[1].strip() if len(text.split()) > 1 else None
            if param:
                if Rates.check(param):
                    curr = Rates(param)
                    text = curr.text()
                else:
                    text =f'Курса для валюты "{param}" на NBRB.BY нет.'
            else:
                # text = 'Список всех доступных валют \n \n' + Rates.all_currencies()
                buttons = [[{'text': 'Долар США', 'callback_data': 'USD'}, {'text': 'Евро', 'callback_data': 'EUR'},
                            {'text': 'Российский рубль', 'callback_data': 'RUB'}],
                           [{'text': 'Показать все доступные валюты', 'callback_data': 'showall'}]]
                reply_markup = {'inline_keyboard': buttons}
                reply_markup = json.dumps(reply_markup)
                params = {'chat_id': chat_id, 'text': 'Выберите валюту', "reply_markup": reply_markup}
                requests.get(url=self.url + '/sendMessage', params=params)
                return None
        return {"chat_id": chat_id, "text": text}

    def send_message(self, chat_id, text):
        text = text
        params = {'chat_id':chat_id, 'text':text}
        req = requests.get(url=self.url+'/sendMessage', params=params)
        print(text)
        if not req.json()['ok']:
            return {"error": req['description']}
        return req.json()

    def callback_query(self, last_update):
        message_id = last_update['callback_query']['message']['message_id']
        chat_id = last_update['callback_query']['message']['chat']['id']
        data = last_update['callback_query']['data']
        print('data', data)
        if data == 'showall':
            #формируем кнопки
            listcurr = Rates.all_currencies_list()
            buttons = []
            buttonsrow = []
            for i, item in enumerate(listcurr):
                buttonsrow.append({'text': f'{item[0]} {item[1]}', 'callback_data': item[1]})
                if (i + 1) % 3 == 0:
                    buttons.append(buttonsrow)
                    buttonsrow = []
            if buttonsrow != []:
                buttons.append(buttonsrow)
            # формируем кнопки
            reply_markup = {'inline_keyboard': buttons}
            reply_markup = json.dumps(reply_markup)
            params = {'chat_id': chat_id, 'message_id': message_id, 'text': 'Выберите валюту',
                      'reply_markup': reply_markup}
            requests.get(url=self.url + '/editMessageText', params=params)
        elif data in Rates.all_currencies_abblist():
            curr = Rates(data)
            text = curr.text()
            buttons = [[{'text': 'Долар США', 'callback_data': 'USD'}, {'text': 'Евро', 'callback_data': 'EUR'},
                        {'text': 'Российский рубль', 'callback_data': 'RUB'}],
                       [{'text': 'Показать все доступные валюты', 'callback_data': 'showall'}]]
            reply_markup = {'inline_keyboard': buttons}
            reply_markup = json.dumps(reply_markup)
            params = {'chat_id': chat_id, 'message_id': message_id, 'text': text,
                      'reply_markup': reply_markup}
            requests.get(url=self.url + '/editMessageText', params=params)
