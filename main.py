import os
import time
from dotenv import load_dotenv

from bot import Bot

# load_dotenv()

# token = os.getenv('TELEGRAM_TOKEN_BOT1')
token = '2088243121:AAFnJa3Xau3z5hbJzatAy2nlGi-a15XnFPY'
bot = Bot(token)

while True:
    message = bot.get_message()
    if message is not None:
        bot.send_message(message['chat_id'], message['text'])
    time.sleep(5)
