from aiogram.dispatcher import FSMContext

from loader import dp
from aiogram import types


@dp.callback_query_handler(text='cancel', state="*")
async def cancel(query: types.CallbackQuery, state: FSMContext):
    await query.message.delete()
    await state.reset_state()