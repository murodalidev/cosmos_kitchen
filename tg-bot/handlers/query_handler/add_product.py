from aiogram.dispatcher import FSMContext

from funcs import get_categories
from keyboards import categories_waiter
from loader import dp
from aiogram import types
from callback_datas import add_product_waiter
from messages import strings


@dp.callback_query_handler(add_product_waiter.filter(filter="add_product_waiter"))
async def add_product(query: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await query.message.delete()
    order_id = int(callback_data.get("order_id"))
    await query.message.answer(
        text=strings['category_request'],
        reply_markup=await categories_waiter(data=await get_categories())
    )
    await state.update_data(order_id=order_id)
