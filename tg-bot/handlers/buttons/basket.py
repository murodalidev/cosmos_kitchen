from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from callback_datas import basket_waiter, basket_supplier
from filters import is_verified
from funcs import all_basket, basket_supp
from loader import dp, users
from messages import strings


@dp.message_handler(is_verified(), Text(equals="Savat"), state="*")
async def basket(message: types.Message, state: FSMContext):
    await state.reset_state()
    data = await users.find_one({"user_id": message.from_user.id})
    if data['rights'][0] == "Ombor":
        data = await basket_supp(user_id=message.from_user.id)
        info = []
        delete_keyboard = types.InlineKeyboardMarkup(row_width=5)
        if data is False:
            await message.answer(
                text=strings['empty_basket']
            )
        else:
            for index, item in enumerate(data):
                delete_keyboard.insert(
                    types.InlineKeyboardButton(text=f"{index + 1} ❌",
                                               callback_data=basket_supplier.new(product_id=item['product_id']))
                )
                info.append(
                    f"<b>{index + 1}.</b> {item['title']} x {item['quantity']}\n"
                )
            delete_keyboard.add(
                types.InlineKeyboardButton(text="🗑 Savatni tozalash", callback_data="clear_supplier")
            )
            delete_keyboard.add(
                types.InlineKeyboardButton(text="Omborni to'ldirish", callback_data="create_supplier")
            )
            await message.answer(
                text="".join(info),
                reply_markup=delete_keyboard
            )
    else:
        data = await all_basket(user_id=message.from_user.id)
        info = []
        delete_keyboard = types.InlineKeyboardMarkup(row_width=5)
        if not data:
            await message.answer(
                text=strings['empty_basket']
            )
        else:
            for index, item in enumerate(data):
                delete_keyboard.insert(
                    types.InlineKeyboardButton(text=f"{index + 1} ❌", callback_data=basket_waiter.new(product_id=item['product_id']))
                )
                info.append(
                    f"<b>{index + 1}.</b> {item['title']} x {item['quantity']} dona\n"
                )
            delete_keyboard.add(
                types.InlineKeyboardButton(text="🗑 Savatni tozalash", callback_data="clear")
            )
            delete_keyboard.add(
                types.InlineKeyboardButton(text="Yangi buyurtma yaratish", callback_data="create")
            )
            await message.answer(
                text="".join(info),
                reply_markup=delete_keyboard
            )
