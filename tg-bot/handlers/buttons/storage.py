from aiogram.dispatcher import FSMContext

from callback_datas import cb_supplier
from funcs import categories_supplier
from loader import dp
from aiogram import types
from aiogram.dispatcher.filters import Text
from filters import is_verified, Rights
from messages import strings


@dp.message_handler(is_verified(), Rights(), Text(equals="Ombor"), state="*")
async def storage(message: types.Message, state: FSMContext):
    await state.reset_state()
    data = await categories_supplier()
    if data is False:
        await message.answer(
            text=strings['error']
        )
    else:
        category = types.InlineKeyboardMarkup(row_width=1)
        for item in data:
            category.add(
                types.InlineKeyboardButton(text=item['title'], callback_data=cb_supplier.new(category_id=item['id'], filter="supplier"))
            )
        await message.answer(
            text=strings['category_request'],
            reply_markup=category
        )