import requests
import json
from rates import Rates
import time
from bot import Bot
import telebot

CHATID = "134203883"
URL = 'https://api.telegram.org/bot2088243121:AAFnJa3Xau3z5hbJzatAy2nlGi-a15XnFPY'


def send_message(self, chat_id, text):
    text = text
    params = {'chat_id': chat_id, 'text': text}
    req = requests.get(url=self.url + '/sendMessage', params=params)
    print(text)
    print(req)
    if not req.json()['ok']:
        return {"error": req['description']}
    return req.json()


def send_keyboard():
    # params = {'chat_id': CHATID, 'text': 'Привет ВАСЯ!'}
    keyboard = [{'text': 'ES'}, {'text': 'EN'}]
    reply_markup = {'ReplyKeyboardMarkup': keyboard}

    reply_markup = {'keyboard': keyboard}
    # params = {'chat_id': CHATID, 'reply_markup': reply_markup}
    # params = {'chat_id': CHATID, "reply_markup": {
    #     "keyboard": [[{"text": "FIRST_BUTTON"}], [{"text": "SECOND_BUTTON"}], [{"text": "THIRD_BUTTON"}]]}}
    reply_markup = {'keyboard': keyboard, 'resize_keyboard': True, 'one_time_keyboard': True}
    reply_markup = {
        "keyboard": [[{"text": "1"}], [{"text": "2"}]],
        "resize_keyboard": True,
        "one_time_keyboard": True
    }
    reply_markup = {'keyboard': [['1'], ['2']], 'resize_keyboard': True, 'one_time_keyboard': True}
    print(reply_markup)
    reply_markup = json.dumps(reply_markup)
    print(reply_markup)
    params = {'chat_id': CHATID, 'text': 'text', "reply_markup": reply_markup}
    # params = {'chat_id': CHATID, 'text': "text"}
    # params = {'chat_id': CHATID, 'text': "text"}
    # req = requests.get(url=self.url + '/sendMessage', params=params)
    # print(text)
    # print(req)
    # if not req.json()['ok']:
    #     return {"error": req['description']}
    # return req.json()
    requests.get(url=URL + '/sendMessage', params=params)


def remove_keyboard():
    reply_markup = {'remove_keyboard': True}
    reply_markup = json.dumps(reply_markup)
    params = {'chat_id': CHATID, 'text': 'Квалиатура удалена', "reply_markup": reply_markup}
    requests.get(url=URL + '/sendMessage', params=params)


def send_keyboard_inline():
    inline_keyboard = [[{'text': 'text', 'url': 'https://yandex.ru/'}]]
    inline_keyboard = {'inline_keyboard': [
        [{'text': 'text', "url": "https://yandex.by/"}, {'text': 'text', "url": "https://yandex.by/"}], [
            {'text': 'text', "url": "https://yandex.by/"}, {'text': 'text', "url": "https://yandex.by/"}]]}
    reply_markup = inline_keyboard
    reply_markup = json.dumps(reply_markup)
    params = {'chat_id': CHATID, 'text': 'textfsdfadsfasdfdsafdasfsdafadsfdsaf', "reply_markup": reply_markup}
    requests.get(url=URL + '/sendMessage', params=params)


def send_keyboard_inline_curr():
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
    inline_keyboard = {'inline_keyboard': buttons}
    reply_markup = inline_keyboard
    reply_markup = json.dumps(reply_markup)
    params = {'chat_id': CHATID, 'text': 'textfsdfadsfasdfdsafdasfsdafadsfdsaf', "reply_markup": reply_markup}
    print(params)
    requests.get(url=URL + '/sendMessage', params=params)


def send_keyboard_inline_curr_short():
    buttons = [[{'text': 'Долар США', 'callback_data': 'USD'}, {'text': 'Евро', 'callback_data': 'EUR'},
                {'text': 'Российский рубль', 'callback_data': 'RUB'}],
               [{'text': 'Показать все доступные валюты', 'callback_data': 'showall'}]]
    inline_keyboard = {'inline_keyboard': buttons}
    reply_markup = inline_keyboard
    reply_markup = json.dumps(reply_markup)
    params = {'chat_id': CHATID, 'text': 'Выберите валюту', "reply_markup": reply_markup}
    requests.get(url=URL + '/sendMessage', params=params)
    time.sleep(5)
    token = '2088243121:AAFnJa3Xau3z5hbJzatAy2nlGi-a15XnFPY'
    bot = Bot(token)
    message = bot.get_last_update()
    print(message)
    text = message['callback_query']['data']
    message_id = message['callback_query']['message']['message_id']
    callback_query_id = message['callback_query']['id']
    # params = {'chat_id': CHATID, 'text': text}
    buttons = [[{'text': 'Кнопка 1', 'callback_data': 'USD'},
                {'text': 'Кнопка 2', 'callback_data': 'EUR'},
                {'text': 'Кнопка 3', 'callback_data': 'RUB'}],
               [{'text': 'Большая кнопка', 'callback_data': 'showall'}]]
    inline_keyboard = {'inline_keyboard': buttons}
    reply_markup = inline_keyboard
    reply_markup = json.dumps(reply_markup)
    params = {'chat_id': CHATID, 'message_id':message_id, 'text': 'Обновленные кнопки', 'reply_markup':reply_markup}
    # requests.get(url=URL + '/sendMessage', params=params)
    print(params)
    # requests.get(url=URL + '/answerCallbackQuery', params=params)
    requests.get(url=URL + '/editMessageText', params=params)
