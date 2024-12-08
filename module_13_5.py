from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import asyncio

api = ""
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


kb = ReplyKeyboardMarkup
button = KeyboardButton(text='Информация')
button2 = KeyboardButton(text='Рассчитать')
kb.add(button)
kb.add(button2)


@dp.message_handler(commands=['start'])
async def start_message(message):
    print('Start message')
    await message.answer('Привет! Я бот помогающий Вашему здоровью.'
                         'Нажмите на кнопку "Рассчитать"')


@dp.message_handler(text='Рассчитать')
async def set_age(message):
    await message.answer('Введите свой возраст')
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    try:
        await state.update_data(age=float(message.text))
    except ValueError:
        await message.answer('Введите свой возраст (сколько Вам полных лет)')
        await UserState.growth.set()
    else:
        await message.answer('Введите свой рост (см)')
        await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    try:
        await state.update_data(growth=float(message.text))
    except ValueError:
        await message.answer('Введите свой рост (см)')
        await UserState.weight.set()
    else:
        await message.answer('Введите свой вес (кг)')
        await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    try:
        await state.update_data(weight=float(message.text))
    except ValueError:
        await message.answer('Введите свой вес (кг)')
        await UserState.weight.set()
    else:
        data = await state.get_data()
        result = 10 * data['weight'] + 6.25 * data['growth'] - 5 * data['age'] + 5
        await message.answer(f'Ваша норма калорий {result} в день. Спасибо, что обратились к нам!  ')
        await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
