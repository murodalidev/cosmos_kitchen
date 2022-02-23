from aiogram.dispatcher import FSMContext

from loader import dp
from aiogram import types
from callback_datas import select_supplier
from messages import strings
from states import count_supplier


@dp.callback_query_handler(select_supplier.filter(filter="select_supplier"))
async def select_supplier(query: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await query.message.delete()
    product_id = int(callback_data.get("id"))
    await query.message.answer(
        text=strings['count_request']
    )
    await state.update_data(product_id=product_id)
    await count_supplier.count.set()