from funcs import delete_single_product, orders_today, paginator
from loader import dp
from aiogram import types
from callback_datas import single_waiter, orders_navigation, add_product_waiter
from messages import is_completed


@dp.callback_query_handler(single_waiter.filter(filter="single_waiter"))
async def single_delete(query: types.CallbackQuery, callback_data: dict):
    await query.message.delete()
    product_id = callback_data.get("product_id")
    order_id = callback_data.get("order_id")
    data = await delete_single_product(product_id=product_id, order_id=order_id)
    if data:
        data = await orders_today(user_id=query.from_user.id)
        order = await paginator(data=data, page=1, products_page=1)
        order_navigation = types.InlineKeyboardMarkup(row_width=5)
        info = []
        for index, item in enumerate(order):
            order_id = item['id']
            info.append(
                f"\n<b>{index + 1} buyurtma: </b>\n\n"
                f"\tMaxsulotlar soni: {item['get_cart_items']}\n"
            )
            for i, order in enumerate(item['order_items']):
                print(order)
                info.append(
                    f"\t<b>{i + 1})</b> {order['meal_name']} x {order['quantity']} dona = {order['get_total']}. Xolati: {is_completed[order['is_completed']]}\n"
                )
                order_navigation.insert(types.InlineKeyboardButton(text=str(i + 1) + " 🗑",
                                                                   callback_data=single_waiter.new(
                                                                       product_id=order['id'],
                                                                       order_id=order_id,
                                                                       filter="single_waiter")))
            info.append(
                f"\nJami: {item['get_cart_total']}"
            )
            order_navigation.add(
                types.InlineKeyboardButton(text="➕ Yangi maxsulot qo'shish",
                                           callback_data=add_product_waiter.new(order_id=item['id'], filter="add_product_waiter"))
            )
            order_navigation.add(
                types.InlineKeyboardButton(text="🗑 Buyurtmani o'chirish", callback_data="delete")
            )
        order_navigation.add(
            types.InlineKeyboardButton(text="➡️", callback_data=orders_navigation.new(page=1, location="next",
                                                                                      filter="orders_navigation"))
        )
        await query.message.answer(
            text="".join(info),
            reply_markup=order_navigation
        )