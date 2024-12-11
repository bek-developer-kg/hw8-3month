from aiogram import Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.filters import Command
from products import get_products, get_product_info, confirm_order, cancel_order

async def start_command(message: types.Message):
    products = get_products()
    keyboard = InlineKeyboardMarkup(inline_keyboard=[])
    for key, product in products.items():
        keyboard.inline_keyboard.append(
            [InlineKeyboardButton(text=product["name"], callback_data=key)]
        )
    await message.answer("Добро пожаловать! Выберите товар:", reply_markup=keyboard)

async def help_command(message: types.Message):
    await message.answer("/start - Начать работу\n/help - Помощь\n/cancel - Отмена заказа")

async def cancel_command(message: types.Message):
    cancel_order(message.from_user.id)
    await message.answer("Ваш заказ отменён. Возвращаемся в главное меню.")
    await start_command(message)

async def product_selection(callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    product_key = callback_query.data

    if product_key.startswith("product_"):
        product_info = get_product_info(user_id, product_key)
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Подтвердить заказ", callback_data="confirm_order")]
        ])
        await callback_query.message.answer(
            f"Вы выбрали: {product_info['name']}\nОписание: {product_info['desc']}\nЦена: {product_info['price']}",
            reply_markup=keyboard
        )
    elif product_key == "confirm_order":
        order_confirmation = confirm_order(user_id)
        await callback_query.message.answer(order_confirmation)
    await callback_query.answer()

def register_handlers(dp: Dispatcher):
    dp.message.register(start_command, Command("start"))
    dp.message.register(help_command, Command("help"))
    dp.message.register(cancel_command, Command("cancel"))
    dp.callback_query.register(product_selection)
