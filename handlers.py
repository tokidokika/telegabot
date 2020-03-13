import datetime
from glob import glob
import os

from random import choice

import ephem
import logging

from utils import get_keyboard, get_user_smile

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
        'Moon': ephem.Moon,
        'Sun': ephem.Sun
        
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

def change_avatar(bot, update, user_data):
    if 'smile' in user_data:
        del user_data['smile']
    smile = get_user_smile(user_data)
    update.message.reply_text(f'Готово: {smile}')

def check_user_photo(bot, update, user_data):
    update.message.reply_text('Обрабатываю фото')
    os.mkdir('downloads', exist_ok=True)
    photo_file = bot.getFile(update.message.photo[-1].file_id)
    filename = os.path.join('downloads', '{}.jpg'.format(photo_file.file_id))
    print(filename)
    # photo_file.download(filename)
    # update