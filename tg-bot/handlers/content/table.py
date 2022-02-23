from aiogram import types
from aiogram.dispatcher import FSMContext

from funcs import create_order
from loader import dp
from messages import strings
from states import count_state


@dp.message_handler(content_types="text", state=count_state.table)
async def get_table(message: types.Message, state: FSMContext):
    table = message.text
    if table.isdigit():
        await create_order(user_id=message.from_user.id, table=int(table))
        await state.reset_state()
        await message.answer(
            text=strings['order_created']
        )
    else:
        await message.answer(
            text=strings['digits_error']
        )