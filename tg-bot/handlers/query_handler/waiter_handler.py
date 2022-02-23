from funcs import get_products, paginator
from loader import dp
from aiogram import types
from callback_datas import cb_waiter, navigation_waiter, select_waiter


@dp.callback_query_handler(cb_waiter.filter(filter="waiter"))
async def waiter_handler(query: types.CallbackQuery, callback_data: dict):
    await query.message.delete()
    p = []
    data = await get_products(category_id=callback_data.get('id'))
    products = await paginator(data=data, page=1, products_page=5)
    if len(data) % 5 != 0:
        max_pages = len(data) // 5 + 1
    else:
        max_pages = len(data) // 5
    navigation = types.InlineKeyboardMarkup(row_width=5)
    for index, item in enumerate(products):
        p.append(
            f"<b>{index + 1}.</b> {item['title']}\n"
        )
        navigation.insert(
            types.InlineKeyboardButton(text=str(index+1), callback_data=select_waiter.new(id=item['id'], filter="select_waiter"))
        )
    if max_pages != 1:
        navigation.add(
            types.InlineKeyboardButton(
                text="➡️",
                callback_data=navigation_waiter.new(page=1, location="next", category_id=callback_data.get('id'), filter="navigation_waiter"))
        )
    await query.message.answer(
        text=f"1/{max_pages} saxifa\n\n" + "".join(p),
        reply_markup=navigation
    )


