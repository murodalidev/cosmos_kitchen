from funcs import orders_today, paginator
from loader import dp
from aiogram import types
from callback_datas import orders_navigation, single_waiter, add_product_waiter
from messages import is_completed, strings


@dp.callback_query_handler(orders_navigation.filter(filter="orders_navigation"))
async def order_navigation(query: types.CallbackQuery, callback_data: dict):
    location = callback_data.get("location")
    page = int(callback_data.get("page"))
    data = await orders_today(user_id=query.from_user.id)
    navigation = types.InlineKeyboardMarkup(row_width=5)
    max_pages = len(data)
    if location == "next":
        info = []
        current_page = page + 1
        order = await paginator(data=data, page=current_page, products_page=1)
        for index, item in enumerate(order):
            order_id = item['id']
            info.append(
                f"\n<b>{order_id} buyurtma: </b>\n\n"
                f"\tMaxsulotlar soni: {item['get_cart_items']}\n"
            )
            for i, order in enumerate(item['order_items']):
                info.append(
                    f"\t<b>{i + 1})</b> {order['meal_name']} x {order['quantity']} dona = {order['get_total']}. Xolati: {is_completed[order['is_completed']]}\n"
                )
                navigation.insert(types.InlineKeyboardButton(text=str(i + 1) + " 🗑",
                                                             callback_data=single_waiter.new(
                                                                 product_id=order['id'],
                                                                 order_id=order_id,
                                                                 filter="single_waiter")))
            info.append(
                f"\nJami: {item['get_cart_total']}"
            )
            navigation.add(
                types.InlineKeyboardButton(text="➕ Yangi maxsulot qo'shish",
                                           callback_data=add_product_waiter.new(order_id=order_id,
                                                                                filter="add_product_waiter"))
            )
        if current_page == max_pages:
            navigation.add(
                types.InlineKeyboardButton(
                    text="⬅️",
                    callback_data=orders_navigation.new(page=current_page, location="prev", filter="orders_navigation"))
            )
        else:
            navigation.add(
                types.InlineKeyboardButton(
                    text="⬅️",
                    callback_data=orders_navigation.new(page=current_page, location="prev",
                                                        filter="orders_navigation")),
                types.InlineKeyboardButton(
                    text="➡️",
                    callback_data=orders_navigation.new(page=current_page, location="next",
                                                        filter="orders_navigation")),
            )
        await query.message.edit_text(
            text="".join(info),
            reply_markup=navigation
        )
    elif location == "prev":
        info = []
        current_page = page - 1
        order = await paginator(data=data, page=current_page, products_page=1)
        for index, item in enumerate(order):
            order_id = item['id']
            info.append(
                f"\n<b>{order_id} buyurtma: </b>\n\n"
                f"\tMaxsulotlar soni: {item['get_cart_items']}\n"
            )
            for i, order in enumerate(item['order_items']):
                info.append(
                    f"\t<b>{i + 1})</b> {order['meal_name']} x {order['quantity']} dona = {order['get_total']}. Xolati: {is_completed[order['is_completed']]}\n"
                )
                navigation.insert(types.InlineKeyboardButton(text=str(i + 1) + " 🗑",
                                                             callback_data=single_waiter.new(
                                                                 product_id=order['id'],
                                                                 order_id=order_id,
                                                                 filter="single_waiter")))
            info.append(
                f"\nJami: {item['get_cart_total']}\nXolati: {item['status_name']}"
            )
            navigation.add(
                types.InlineKeyboardButton(text="➕ Yangi maxsulot qo'shish",
                                           callback_data=add_product_waiter.new(order_id=order_id,
                                                                                filter="add_product_waiter"))
            )
        if current_page == 1:
            navigation.add(
                types.InlineKeyboardButton(
                    text="➡️",
                    callback_data=orders_navigation.new(page=current_page, location="next", filter="orders_navigation")),
            )
        else:
            navigation.add(
                types.InlineKeyboardButton(
                    text="⬅️",
                    callback_data=orders_navigation.new(page=current_page, location="prev", filter="orders_navigation")),
                types.InlineKeyboardButton(
                    text="➡️",
                    callback_data=orders_navigation.new(page=current_page, location="next", filter="orders_navigation")),
            )
        await query.message.edit_text(
            text="".join(info),
            reply_markup=navigation
        )
