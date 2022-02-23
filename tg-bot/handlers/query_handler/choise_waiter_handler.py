from aiogram.dispatcher import FSMContext

from loader import dp
from aiogram import types
from callback_datas import choise_waiter, count_waiter
from messages import strings
from states import count_state


@dp.callback_query_handler(choise_waiter.filter(filter='choise_waiter'))
async def choise_waiter_handler(query: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await query.message.delete()
    await state.update_data(product_id=int(callback_data.get("id")))
    count_keyboard = types.InlineKeyboardMarkup(row_width=3)
    for i in range(1, 10):
        count_keyboard.insert(types.InlineKeyboardButton(text=str(i), callback_data=count_waiter.new(count=i)))
    await query.message.answer(
        text=strings['count_user'],
        reply_markup=count_keyboard
    )
    await count_state.count.set()