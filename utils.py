from random import choice

from clarifai.rest import ClarifaiApp
from telegram import ReplyKeyboardMarkup, KeyboardButton
from emoji import emojize

USER_EMOJI = [':smiley_cat:', ':smiling_imp:', ':panda_face:', ':dog:']

CLARIFAI_API_KEY = '907c4c77d95543e18e3f50a804209bce'


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


def is_cat(file_name):
    image_has_cat = False
    app = ClarifaiApp(api_key=CLARIFAI_API_KEY)
    model = app.public_models.general_model
    response = model.predict_by_filename(file_name, max_concepts=5)
    if response['status']['code'] == 10000:
        for concept in response['outputs'][0]['data']['concepts']:
            if concept['name'] == 'cat':
                image_has_cat = True
    return image_has_cat


if __name__ == "__main__":
    print(is_cat('images/cat_cute.jpg'))