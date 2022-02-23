from aiogram.dispatcher import FSMContext

from funcs import product_detail
from loader import dp
from aiogram import types
from callback_datas import select_waiter, choise_waiter
from states import count_state


@dp.callback_query_handler(select_waiter.filter(filter="select_waiter"))
async def select(query: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await query.message.delete()
    product_id = int(callback_data.get('id'))
    data = await product_detail(product_id=product_id)
    select_keyboard = types.InlineKeyboardMarkup(row_width=1)
    select_keyboard.add(
        types.InlineKeyboardButton(text="Savatga qo'shish", callback_data=choise_waiter.new(id=product_id, filter="choise_waiter"))
    )
    await query.message.answer_photo(
        photo=data['get_image_url'],
        caption=f"<b>Kategoriya: </b> {data['category_name']}\n\n"
                f"<b>Nomi: </b> {data['title']}\n"
                f"<b>Narxi: </b> {data['cost']}",
        reply_markup=select_keyboard
    )
