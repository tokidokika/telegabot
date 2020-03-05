from random import choice

from telegram import ReplyKeyboardMarkup, KeyboardButton
from emoji import emojize

USER_EMOJI = [':smiley_cat:', ':smiling_imp:', ':panda_face:', ':dog:']


def get_user_smile(user_data):
    if 'smile' in user_data:
        return user_data['smile']
    else:
        user_data['smile'] = emojize(choice(USER_EMOJI), use_aliases=True)
        return user_data['smile']

def get_keyboard():
    contact_button = KeyboardButton("Прислать контакты", request_contact=True)
    location_button = KeyboardButton("Прислать локацию", request_location=True)
    my_keyboard = ReplyKeyboardMarkup([
                                        ["Прислать котика", "Сменить смайлик"], 
                                        [contact_button, location_button]
                                      ], resize_keyboard=True
                                     )
    return my_keyboard