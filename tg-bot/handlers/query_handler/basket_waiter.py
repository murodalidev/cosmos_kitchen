from funcs import delete_product, all_basket, delete_all, create_order
from loader import dp
from aiogram import types
from callback_datas import basket_waiter
from messages import strings
from states import count_state


@dp.callback_query_handler(basket_waiter.filter())
async def basket_waiter_handler(query: types.CallbackQuery, callback_data: dict):
    product_id = int(callback_data.get("product_id"))
    await delete_product(product_id=product_id)
    await query.message.delete()
    data = await all_basket(user_id=query.from_user.id)
    info = []
    delete_keyboard = types.InlineKeyboardMarkup(row_width=5)
    if not data:
        await query.message.answer(
            text=strings['empty_basket']
        )
    else:
        for index, item in enumerate(data):
            delete_keyboard.insert(
                types.InlineKeyboardButton(text=f"{index + 1} ❌",
                                           callback_data=basket_waiter.new(product_id=item['product_id']))
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
        await query.message.answer(
            text="".join(info),
            reply_markup=delete_keyboard
        )


@dp.callback_query_handler(text="clear")
async def clear_basket(query: types.CallbackQuery):
    await delete_all(user_id=query.from_user.id)
    await query.message.delete()
    await query.message.answer(
        text=strings['empty_basket']
    )


@dp.callback_query_handler(text="create")
async def create(query: types.CallbackQuery):
    await query.message.edit_text(
        text=strings['table_number']
    )
    await count_state.table.set()