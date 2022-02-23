from aiogram import types

from funcs import products_supplier, paginator
from loader import dp
from callback_datas import navigation_supplier, select_supplier
from messages import strings


@dp.callback_query_handler(navigation_supplier.filter(filter="navigation_supplier"))
async def navigation_waiter_handler(query: types.CallbackQuery, callback_data: dict):
    location = callback_data.get("location")
    page = int(callback_data.get("page"))
    category_id = int(callback_data.get('category_id'))
    data = await products_supplier(category_id=category_id)
    if len(data) % 5 != 0:
        max_pages = len(data) // 5 + 1
    else:
        max_pages = len(data) // 5
    if location == "next":
        current_page = page + 1
        products = await paginator(data=data, page=current_page, products_page=5)
        p = []
        navigation = types.InlineKeyboardMarkup(row_width=5)
        for index, item in enumerate(products):
            p.append(
                f"{index + 1}. {item['title']}\n"
            )
            navigation.insert(
                types.InlineKeyboardButton(text=f"{index + 1}",
                                           callback_data=select_supplier.new(id=item['id'], filter="select_supplier"))
            )
        if current_page == max_pages:
            navigation.add(
                types.InlineKeyboardButton(
                    text="⬅️",
                    callback_data=navigation_supplier.new(page=current_page, location="prev", category_id=category_id, filter="navigation_supplier"))
            )
        else:
            navigation.add(
                types.InlineKeyboardButton(
                    text="⬅️",
                    callback_data=navigation_supplier.new(page=current_page, location="prev", category_id=category_id, filter="navigation_supplier")),
                types.InlineKeyboardButton(
                    text="➡️",
                    callback_data=navigation_supplier.new(page=current_page, location="next", category_id=category_id, filter="navigation_supplier")),
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
                f"{index + 1}. {item['title']}\n"
            )
            navigation.insert(
                types.InlineKeyboardButton(text=f"{index + 1}",
                                           callback_data=select_supplier.new(id=item['id'], filter="select_supplier"))
            )
        if current_page == 1:
            navigation.add(
                types.InlineKeyboardButton(
                    text="➡️",
                    callback_data=navigation_supplier.new(page=current_page, location="next", category_id=category_id, filter="navigation_supplier")),
            )
        else:
            navigation.add(
                types.InlineKeyboardButton(
                    text="⬅️",
                    callback_data=navigation_supplier.new(page=current_page, location="prev", category_id=category_id, filter="navigation_supplier")),
                types.InlineKeyboardButton(
                    text="➡️",
                    callback_data=navigation_supplier.new(page=current_page, location="next", category_id=category_id, filter="navigation_supplier")),
            )
        await query.message.edit_text(
            text=f"{current_page}/{max_pages} saxifa\n\n" + "".join(p),
            reply_markup=navigation
        )

