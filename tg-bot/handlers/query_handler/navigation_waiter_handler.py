from aiogram import types

from funcs import get_products, paginator
from loader import dp
from callback_datas import navigation_waiter, select_waiter


@dp.callback_query_handler(navigation_waiter.filter(filter="navigation_waiter"))
async def navigation_waiter_handler(query: types.CallbackQuery, callback_data: dict):
    location = callback_data.get("location")
    page = int(callback_data.get("page"))
    category_id = int(callback_data.get('category_id'))
    data = await get_products(category_id=category_id)
    if len(data) % 5 != 0:
        max_pages = len(data) // 5 + 1
    else:
        max_pages = len(data) // 5
    if location == "next":
        current_page = page + 1
        products = await paginator(data=data, page=current_page, products_page=5)
        navigation = types.InlineKeyboardMarkup(row_width=5)
        p = []
        for index, item in enumerate(products):
            p.append(
                f"<b>{index + 1}.</b> {item['title']}. (<b>{item['category_name']}</b>)\n"
            )
            navigation.insert(
                types.InlineKeyboardButton(text=str(index + 1),
                                           callback_data=select_waiter.new(id=item['id'], filter="select_waiter"))
            )
        if current_page == max_pages:
            navigation.add(
                types.InlineKeyboardButton(
                    text="⬅️",
                    callback_data=navigation_waiter.new(page=current_page, location="prev", category_id=category_id, filter="navigation_waiter"))
            )
        else:
            navigation.add(
                types.InlineKeyboardButton(
                    text="⬅️",
                    callback_data=navigation_waiter.new(page=current_page, location="prev", category_id=category_id, filter="navigation_waiter")),
                types.InlineKeyboardButton(
                    text="➡️",
                    callback_data=navigation_waiter.new(page=current_page, location="next", category_id=category_id, filter="navigation_waiter")),
            )
        await query.message.edit_text(
            text=f"{current_page}/{max_pages} saxifa\n\n" + "".join(p),
            reply_markup=navigation
        )
    elif location == "prev":
        current_page = page - 1
        products = await paginator(data=data, page=current_page, products_page=5)
        navigation = types.InlineKeyboardMarkup(row_width=5)
        p = []
        for index, item in enumerate(products):
            p.append(
                f"<b>{index + 1}.</b> {item['title']}. (<b>{item['category_name']}</b>)\n"
            )
            navigation.insert(
                types.InlineKeyboardButton(text=str(index + 1),
                                           callback_data=select_waiter.new(id=item['id'], filter="select_waiter"))
            )
        if current_page == 1:
            navigation.add(
                types.InlineKeyboardButton(
                    text="➡️",
                    callback_data=navigation_waiter.new(page=current_page, location="next", category_id=category_id, filter="navigation_waiter")),
            )
        else:
            navigation.add(
                types.InlineKeyboardButton(
                    text="⬅️",
                    callback_data=navigation_waiter.new(page=current_page, location="prev", category_id=category_id, filter="navigation_waiter")),
                types.InlineKeyboardButton(
                    text="➡️",
                    callback_data=navigation_waiter.new(page=current_page, location="next", category_id=category_id, filter="navigation_waiter")),
            )
        await query.message.edit_text(
            text=f"{current_page}/{max_pages} saxifa\n\n" + "".join(p),
            reply_markup=navigation
        )

