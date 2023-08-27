from aiogram import types, Dispatcher, Bot
from aiogram.utils import executor
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from credits import token
import random
from emoji import emojize


bot = Bot(token=token, parse_mode="HTML")
dp = Dispatcher(bot, storage=MemoryStorage())

emoji_codes = {'камень': '',
               'ножницы': '',
               'бумага': ''}

class EasyCode(StatesGroup):
    waiting_for_step = State()


async def start(message: types.Message):
    await message.answer('<s>Привет!</s> Я - бот КНБ. Напиши /game, чтобы начать игру')


async def game(message: types.Message, state: FSMContext):
    await message.answer('Игра началась. Твой ход!')
    await state.update_data(user_points=0)
    await state.update_data(comp_points=0)
    await EasyCode.waiting_for_step.set()


async def step(message: types.Message, state: FSMContext):
    user = message.text.lower()
    comp = random.choice(['камень', 'ножницы', 'бумага'])
    data = await state.get_data()
    user_points = int(data.get('user_points'))
    comp_points = int(data.get('comp_points'))
    print(user_points, comp_points)
    if user == 'камень' and comp == 'бумага' or user == 'ножницы' and comp == 'камень' or user == 'бумага' and comp == 'ножницы':
        comp_points += 1
        await state.update_data(comp_points = str(comp_points))
        await message.answer(f'''Твой выбор: {user}.
Мой выбор: {comp}.
Я победил!
Человек - {user_points} : {comp_points} - Бот.''')
    elif user == 'камень' and comp == 'ножницы' or user == 'ножницы' and comp == 'бумага' or user == 'бумага' and comp == 'камень':
        user_points += 1
        await state.update_data(user_points = str(user_points))
        await message.answer(f'''Твой выбор: {user}.
Мой выбор: {comp}.
Ты победил!
Человек - {user_points} : {comp_points} - Бот.''')
    else:
        await message.answer(f'''В ничью сыграли. Давай по новой. Текущий счёт:
Человек - {user_points} : {comp_points} - Бот.''')
        

    if user_points == 3 or comp_points == 3:
        await message.answer(f'В игре до трё побед победил {"бот" if comp_points > user_points else "ты"}. Спасибо за игру! Пиши /game, чтобы начать заново.')
        await state.finish()



def register_handlers(dp: Dispatcher):
    dp.register_message_handler(start, commands="start", state="*")
    dp.register_message_handler(game, commands="game", state='*')
    dp.register_message_handler(step, state=EasyCode.waiting_for_step)



register_handlers(dp)

executor.start_polling(dp, skip_updates=True)