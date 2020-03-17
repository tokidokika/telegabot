import datetime
from glob import glob
import os

from random import choice

import ephem
import logging

from telegram import ReplyKeyboardRemove, ReplyKeyboardMarkup, ParseMode
from telegram.ext import ConversationHandler

from utils import get_keyboard, get_user_smile, is_cat

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
    os.makedirs('downloads', exist_ok=True)
    photo_file = bot.getFile(update.message.photo[-1].file_id)
    filename = os.path.join('downloads', '{}.jpg'.format(photo_file.file_id))
    photo_file.download(filename)
    if is_cat(filename):
        update.message.reply_text("Обнаружен котик, добавляю в библиотеку.")
        new_filename = os.path.join('images', 'cat_{}.jpg'.format(photo_file.file_id))
        os.rename(filename, new_filename)
    else:
        os.remove(filename)
        update.message.reply_text("Котика нет")


def anketa_start(bot, update, user_data):
    update.message.reply_text("Как вас зовут? Напишите имя и фамилию", reply_markup=ReplyKeyboardRemove())
    return "name"

def anketa_get_name(bot, update, user_data):
    user_name = update.message.text
    if len(user_name.split(" ")) != 2:
        update.message.reply_text("Пожалуйста, введите имя и фамилию")
        return "name"
    else:
        user_data['anketa_name'] = user_name
        reply_keyboard = [["1", "2", "3", "4", "5"]]                       # клавиши на клавиатуре могут быть только строками

        update.message.reply_text(
            "Оцените нашего бота от 1 до 5", 
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
        )
        return "rating"

def anketa_rating(bot, update, user_data):
    user_data['anketa_rating'] = update.message.text
    # для переноса строк внутри текста, нужно ставить тройные кавычки
    update.message.reply_text("""Пожалуста, напишите отзыв в свободной форме     
или /cancel чтобы пропустить этот шаг""")
    return "comment"
    
def anketa_comment(bot, update, user_data):
    user_data['anketa_comment'] = update.message.text
    text = """
<b>Фамилия Имя:</b> {anketa_name}
<b>Оценка:</b> {anketa_rating}
<b>Комментарий:</b> {anketa_comment}""".format(**user_data)
    update.message.reply_text(text, reply_markup=get_keyboard(), parse_mode=ParseMode.HTML)
    return ConversationHandler.END

def anketa_skip_comment(bot, update, user_data):
    text = """
<b>Фамилия Имя:</b> {anketa_name}
<b>Оценка:</b> {anketa_rating}""".format(**user_data)
    update.message.reply_text(text, reply_markup=get_keyboard(), parse_mode=ParseMode.HTML)
    return ConversationHandler.END

def dontknow(bot, update, user_data):
    update.message.reply_text("Не понимаю")
