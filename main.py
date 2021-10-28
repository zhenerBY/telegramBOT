import os
import time
# from dotenv import load_dotenv

from bot import Bot

# load_dotenv()

# token = os.getenv('TELEGRAM_TOKEN_BOT1')
token = '2088243121:AAFnJa3Xau3z5hbJzatAy2nlGi-a15XnFPY'
bot = Bot(token)

if __name__ == '__main__':
    while True:
        last_update = bot.get_last_update()
        if last_update is not None:
            if list(last_update.keys())[1] == 'message':
                params = bot.get_message(last_update)
                if params is not None:
                    method = '/sendMessage'
                    bot.send(method=method, params=params)
            elif list(last_update.keys())[1] == 'callback_query':
                bot.callback_query(last_update)
        time.sleep(0.5)
