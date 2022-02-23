from aiogram.dispatcher import FSMContext

from funcs import product_detail, update_order
from loader import dp
from aiogram import types
from callback_datas import count_waiter, cb_confirm
from messages import strings
from states import count_state


@dp.callback_query_handler(count_waiter.filter(), state=count_state.count)
async def count_waiter(query: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await query.message.delete()
    count = int(callback_data.get('count'))
    product_id = int((await state.get_data()).get("product_id"))
    order_id = (await state.get_data()).get("order_id")
    if order_id is not None:
        if await update_order(order_id=int(order_id), product_id=product_id, quantity=count):
            await query.message.answer(
                text=strings['order_updated']
            )
        else:
            await query.message.answer(
                text=strings['error']
            )
    else:
        confirm_keyboard = types.InlineKeyboardMarkup(row_width=2)
        confirm_keyboard.add(
            types.InlineKeyboardButton(text="Davom etish",
                                       callback_data=cb_confirm.new(count=count, product_id=product_id)),
            types.InlineKeyboardButton(text="Bekor qilish", callback_data="cancel")
        )
        await query.message.answer(
            text=strings['confirm'].format((await product_detail(product_id=product_id))['title'], count),
            reply_markup=confirm_keyboard
        )
        await state.reset_state()


@dp.message_handler(content_types="text", state=count_state.count)
async def count_waiter(message: types.Message, state: FSMContext):
    count = message.text
    product_id = int((await state.get_data()).get("product_id"))
    order_id = (await state.get_data()).get("order_id")
    if count == 0:
        await message.answer(
            text=strings['digit_error']
        )
    elif count.isdigit():
        if order_id is not None:
            if await update_order(order_id=int(order_id), product_id=product_id, quantity=count):
                await message.answer(
                    text=strings['order_updated']
                )
            else:
                await message.answer(
                    text=strings['error']
                )
        else:
            confirm_keyboard = types.InlineKeyboardMarkup(row_width=2)
            confirm_keyboard.add(
                types.InlineKeyboardButton(text="Davom etish",
                                           callback_data=cb_confirm.new(count=count, product_id=product_id)),
                types.InlineKeyboardButton(text="Bekor qilish", callback_data="cancel")
            )
            await message.answer(
                text=strings['confirm'].format((await product_detail(product_id=product_id))['title'], count),
                reply_markup=confirm_keyboard
            )
            await state.reset_state()
    else:
        await message.answer(
            text=strings['digits_error']
        )