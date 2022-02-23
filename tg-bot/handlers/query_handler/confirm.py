from aiogram import types

from callback_datas import cb_confirm
from funcs import add_basket, product_detail, get_categories
from keyboards import categories_waiter
from loader import dp
from messages import strings


@dp.callback_query_handler(cb_confirm.filter())
async def confirm(query: types.CallbackQuery, callback_data: dict):
    await query.message.delete()
    count = int(callback_data.get("count"))
    product_id = int(callback_data.get("product_id"))
    title = await product_detail(product_id=product_id)
    await add_basket(user_id=query.from_user.id, product_id=product_id, quantity=count, title=title['title'])
    await query.message.answer(
        text=strings['basket']
    )
    await query.message.answer(
        text=strings['category_request'],
        reply_markup=await categories_waiter(data=await get_categories())
    )
