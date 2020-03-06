import logging

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, RegexHandler
from handlers import *


PROXY = {'proxy_url': 'socks5://t1.learn.python.ru:1080',
    'urllib3_proxy_kwargs': {'username': 'learn', 'password': 'python'}}

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot.log'
                    )

def main():
    mybot = Updater('API_KEy', request_kwargs=PROXY)

    dp = mybot.dispatcher

    dp.add_handler(CommandHandler("start", greet_user, pass_user_data=True))
    dp.add_handler(CommandHandler("planet", about_planet, pass_user_data=True))
    dp.add_handler(CommandHandler("cat", send_cat_picture, pass_user_data=True))
    dp.add_handler(RegexHandler('^(Прислать котика)$', send_cat_picture, pass_user_data=True))
    dp.add_handler(RegexHandler('^(Сменить смайлик)$', change_avatar, pass_user_data=True))

    dp.add_handler(MessageHandler(Filters.text, talk_to_me, pass_user_data=True))
    dp.add_handler(MessageHandler(Filters.contact, get_contact, pass_user_data=True))
    dp.add_handler(MessageHandler(Filters.location, get_location, pass_user_data=True))
    
    mybot.start_polling()
    mybot.idle()

if __name__=='__main__':
    main()