from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


start_menu = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='Профиль', callback_data='st_profile'),
        InlineKeyboardButton(text='О нас', callback_data='about')
    ],
    [
        InlineKeyboardButton(text='Реферальная система', callback_data='ref_system'),
        InlineKeyboardButton(text='Калькулятор', callback_data='calc')
    ]
])

profil_menu = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='Внести депозит', callback_data='up_balance'),
        InlineKeyboardButton(text='Вывести баланс', callback_data='down_balance')
    ]
])

for_admin_menu = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='Участники бота', callback_data='all_users'),
        InlineKeyboardButton(text='Изменить баланс', callback_data='change_balance')
    ]
])

back_menu = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='В профиль', callback_data='st_profile'),
        InlineKeyboardButton(text='Реферальная система', callback_data='ref_system')
    ]
])

calc_menu = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='10$ на 7 дней', callback_data='10_7'),
        InlineKeyboardButton(text='50$ на 14 дней', callback_data='50_14')
    ],
    [
        InlineKeyboardButton(text='100$ на 7 дней', callback_data='100_7'),
        InlineKeyboardButton(text='500$ на 14 дней', callback_data='500_14')
    ]
])


