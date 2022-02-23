from aiogram.dispatcher import FSMContext

from funcs import products_supplier, paginator
from loader import dp
from aiogram import types
from callback_datas import cb_supplier, navigation_supplier, select_supplier


@dp.callback_query_handler(cb_supplier.filter(filter="supplier"))
async def supplier_handler(query: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await query.message.delete()
    category_id = int(callback_data.get("category_id"))
    await state.update_data(category_id=category_id)
    data = await products_supplier(category_id=category_id)
    products = await paginator(data=data, page=1, products_page=5)
    if len(data) % 5 != 0:
        max_pages = len(data) // 5 + 1
    else:
        max_pages = len(data) // 5
    p = []
    navigation = types.InlineKeyboardMarkup(row_width=5)
    for index, item in enumerate(products):
        p.append(
            f"{index + 1}. {item['title']}\n"
        )
        navigation.insert(
            types.InlineKeyboardButton(text=f"{index + 1}", callback_data=select_supplier.new(id=item['id'], filter="select_supplier"))
        )
    if max_pages != 1:
        navigation.add(
            types.InlineKeyboardButton(
                text="➡️",
                callback_data=navigation_supplier.new(page=1, location="next", category_id=category_id, filter="navigation_supplier"))
        )
    await query.message.answer(
        text=f"1/{max_pages} saxifa\n\n" + "".join(p),
        reply_markup=navigation
    )