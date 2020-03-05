import datetime
from glob import glob
from random import choice

from emoji import emojize
from telegram import ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, RegexHandler

import ephem
import logging

PROXY = {'proxy_url': 'socks5://t1.learn.python.ru:1080',
    'urllib3_proxy_kwargs': {'username': 'learn', 'password': 'python'}}

USER_EMOJI = [':smiley_cat:', ':smiling_imp:', ':panda_face:', ':dog:']

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot.log'
                    )

def main():
    mybot = Updater('API_KEY', request_kwargs=PROXY)

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

def greet_user(bot, update, user_data):
    smile = get_user_smile(user_data)
    text = f"Привет {smile}"
    update.message.reply_text(text, reply_markup=get_keyboard())

def get_contact(bot, update, user_data):
    print(update.message.contact)
    update.message.reply_text(f'Готово: {get_user_smile(user_data)}')

def get_location(bot, update, user_data):
    print(update.message.location)
    update.message.reply_text(f'Готово: {get_user_smile(user_data)}')

def talk_to_me(bot, update, user_data):
    smile = get_user_smile(user_data)
    user_text = f"Вы ввели {update.message.text} {smile}"
    print(user_text)
    update.message.reply_text(user_text, reply_markup=get_keyboard())

def get_constellation_by_planet(planet):
    date = datetime.datetime.now()
    user_say = planet
    dct = {
        'Pluto': ephem.Pluto,
        'Mercury': ephem.Mercury,
        'Mars': ephem.Mars,
        'Uranus': ephem. Uranus,
        'Jupiter': ephem.Jupiter,
        'Venus': ephem.Venus,
        'Neptune': ephem.Neptune,
        'Moon': ephem.Moon
        
    }
    planet_func = dct[user_say]
    planet_obj = planet_func(date)
    planet_cons = ephem.constellation(planet_obj)
    return planet_cons[1]

def about_planet(bot, update, user_data):
    smile = get_user_smile(user_data)
    plnt = update.message.text
    plnt_name = plnt.split()[1]
    constellation = get_constellation_by_planet(plnt_name)
    print(constellation)
    update.message.reply_text(f"Планета {plnt_name} находится в созвездии {constellation} {smile}", reply_markup=get_keyboard())

def send_cat_picture(bot, update, user_data):
    cat_list = glob('images/cat*.jp*g')
    cat_pic = choice(cat_list)
    bot.send_photo(chat_id=update.message.chat.id, photo=open(cat_pic, 'rb'), reply_markup=get_keyboard())

def get_user_smile(user_data):
    if 'smile' in user_data:
        return user_data['smile']
    else:
        user_data['smile'] = emojize(choice(USER_EMOJI), use_aliases=True)
        return user_data['smile']

def change_avatar(bot, update, user_data):
    if 'smile' in user_data:
        del user_data['smile']
    smile = get_user_smile(user_data)
    update.message.reply_text(f'Готово: {smile}')

def get_keyboard():
    contact_button = KeyboardButton("Прислать контакты", request_contact=True)
    location_button = KeyboardButton("Прислать локацию", request_location=True)
    my_keyboard = ReplyKeyboardMarkup([
                                        ["Прислать котика", "Сменить смайлик"], 
                                        [contact_button, location_button]
                                      ], resize_keyboard=True
                                     )
    return my_keyboard


main()