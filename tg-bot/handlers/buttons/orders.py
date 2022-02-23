from aiogram.dispatcher import FSMContext

from callback_datas import single_waiter, add_product_waiter, orders_navigation
from funcs import orders_today, paginator
from loader import dp
from aiogram import types
from aiogram.dispatcher.filters import Text

from messages import is_completed, strings


@dp.message_handler(Text(equals="Buyurtmalar"), state="*")
async def orders(message: types.Message, state: FSMContext):
    await state.reset_state()
    data = await orders_today(user_id=message.from_user.id)
    if data is False:
        await message.answer(
            text=strings['empty_orders']
        )
    else:
        order = await paginator(data=data, page=1, products_page=1)
        order_navigation = types.InlineKeyboardMarkup(row_width=5)
        info = []
        for index, item in enumerate(order):
            print(item)
            order_id = item['id']
            info.append(
                f"\n<b>{order_id} buyurtma: </b>\n\n"
                f"\tMaxsulotlar soni: {item['get_cart_items']}\n"
            )
            for i, order in enumerate(item['order_items']):
                info.append(
                    f"\t<b>{i + 1})</b> {order['meal_name']} x {order['quantity']} dona = {order['get_total']}. Xolati: {is_completed[order['is_completed']]}\n"
                )
                order_navigation.insert(types.InlineKeyboardButton(text=str(i + 1) + " 🗑",
                                                                   callback_data=single_waiter.new(product_id=order['id'],
                                                                                                   order_id=order_id,
                                                                                                   filter="single_waiter")))
            info.append(
                f"\nJami: {item['get_cart_total']}\nXolati: {item['status_name']}"
            )
            order_navigation.add(
                types.InlineKeyboardButton(text="➕ Yangi maxsulot qo'shish",
                                           callback_data=add_product_waiter.new(order_id=order_id, filter="add_product_waiter"))
            )
        order_navigation.add(
            types.InlineKeyboardButton(text="➡️", callback_data=orders_navigation.new(page=1, location="next",
                                                                                      filter="orders_navigation"))
        )
        await message.answer(
            text="".join(info),
            reply_markup=order_navigation
        )
