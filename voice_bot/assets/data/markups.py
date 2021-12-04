from aiogram.types import InlineKeyboardMarkup,\
    InlineKeyboardButton,ReplyKeyboardMarkup,KeyboardButton
from assets.loader import load_cfg

from db.db import get_me_sticker, get_stick


markups = {
    'not_connect':InlineKeyboardMarkup().add(
        InlineKeyboardButton(
            'Подписаться на канал',url=load_cfg()['link']
        )
    ),
    'started':ReplyKeyboardMarkup(resize_keyboard=True).add(
        KeyboardButton('Mening goloslarim'),
        KeyboardButton('Golos qoshish')
    ).add(
        KeyboardButton('Hamma goloslar'),
        KeyboardButton('Statistika')
    ),
    'started_not_adm':ReplyKeyboardMarkup(resize_keyboard=True).add(
        KeyboardButton('Mening goloslarim'),
        KeyboardButton('Golos qoshish')
    ).add(
        KeyboardButton('Hamma goloslar')
    ),
    'save?':InlineKeyboardMarkup().add(
        InlineKeyboardButton('Xa',callback_data='save'),
        InlineKeyboardButton('Yoq',callback_data='delete')
    ),
    'otmena':InlineKeyboardMarkup().add(InlineKeyboardButton(text='✖️ Bekor qilish',callback_data='error_hundler'))
    }
def del_by_id(_id):
    return InlineKeyboardMarkup().add(InlineKeyboardButton(text='✖️ Ochirib tashlash!',callback_data=f'del|{_id}'))
    
def adm_mark(_id,_id_s):
    return InlineKeyboardMarkup().add(
        InlineKeyboardButton('✅ Qabul qilish',callback_data=f'ok|{_id}|{_id_s}'),
        InlineKeyboardButton('❌ Rad etish',callback_data=f'no|{_id}|{_id_s}')
    )

def generate_list(_id=None):
    markup = InlineKeyboardMarkup()
    if _id:
        for i in get_me_sticker(_id):
            markup.add(InlineKeyboardButton(text=i.name,callback_data=i.id))
        
    else:
        for i in get_stick():
            markup.add(InlineKeyboardButton(text=i.name,callback_data=i.id))
    
    return markup
