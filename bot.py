import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from config import token

bot = Bot(token=token)
dp = Dispatcher(storage=MemoryStorage())

PRODUCTS = {
    "product_1": {
        "name": "Ноутбук HP",
        "desc": "Ноутбук HP Victus 15 Gaming 15.6 144HZ AMD Ryzen 5 8645HS Nvidia GeForce RTX 4050 6gb",
        "price": "69900сом."
    },
    "product_2": {
        "name": "Ноутбук Asus",
        "desc": "Ноутбук ASUS TUF Gaming F15 15.6 144HZ Intel Core i5-10300H GeForce GTX 1650",
        "price": "64000сом."
    },
}

user_orders = {}

class OrderStates(StatesGroup):
    waiting_for_email = State()

@dp.message(Command("start"))
async def start_command(message: types.Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[])
    for key, product in PRODUCTS.items():
        keyboard.inline_keyboard.append(
            [InlineKeyboardButton(text=product["name"], callback_data=key)]
        )
    await message.answer("Добро пожаловать! Выберите товар:", reply_markup=keyboard)

@dp.message(Command("help"))
async def help_command(message: types.Message):
    help_text = (
        "/start - Начать работу\n"
        "/help - Помощь\n"
        "/cancel - Отмена заказа"
    )
    await message.answer(help_text)

@dp.message(Command("cancel"))
async def cancel_command(message: types.Message):
    user_orders.pop(message.from_user.id, None)  # Удаление заказа пользователя
    await message.answer("Ваш заказ отменён. Возвращаемся в главное меню.")
    await start_command(message)

@dp.callback_query()
async def product_selection(callback_query: CallbackQuery, state: FSMContext):
    user_id = callback_query.from_user.id
    product_key = callback_query.data

    if product_key in PRODUCTS:
        product = PRODUCTS[product_key]
        user_orders[user_id] = product

        keyboard = InlineKeyboardMarkup(inline_keyboard=[])
        keyboard.inline_keyboard.append(
            [InlineKeyboardButton(text="Подтвердить заказ", callback_data="confirm_order")]
        )

        await callback_query.message.answer(
            text=f"Вы выбрали: {product['name']}\nОписание: {product['desc']}\nЦена: {product['price']}",
            reply_markup=keyboard,
        )
        await callback_query.answer()

    elif product_key == "confirm_order":
        order = user_orders.get(user_id)
        if order:
            await callback_query.message.answer(
                text=f"Ваш заказ принят:\n{order['name']}\n{order['desc']}\n{order['price']}"
            )
            await state.set_state(OrderStates.waiting_for_email)
            await callback_query.message.answer("Пожалуйста, введите вашу почту для отправки заказа.")
        else:
            await callback_query.message.answer("Сначала выберите товар.")
        await callback_query.answer()

@dp.message(OrderStates.waiting_for_email)
async def process_email(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    user_email = message.text.strip()

    user_orders[user_id]['email'] = user_email

    await send_order_to_email(user_orders[user_id], message)

    user_orders.pop(user_id, None)
    await state.finish()

    await message.answer(f"Ваш заказ был успешно отправлен на почту {user_email}!\n"
                         f"Товар: {user_orders[user_id]['name']}\nОписание: {user_orders[user_id]['desc']}\nЦена: {user_orders[user_id]['price']}")

async def send_order_to_email(order, message: types.Message):
    print(f"--- Имитация отправки на почту ---")
    print(f"Заказ на почту отправлен:\nТовар: {order['name']}\nОписание: {order['desc']}\nЦена: {order['price']}\n"
          f"Отправлено на: {order['email']}")
    print(f"----------------------------------")
    
    await message.answer(f"Ваш заказ был успешно отправлен на почту {order['email']}!\n"
                         f"Товар: {order['name']}\nОписание: {order['desc']}\nЦена: {order['price']}")

# Запуск бота
async def main():
    print("Бот запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
