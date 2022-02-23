from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from funcs import get_categories
from keyboards import categories_waiter
from loader import dp
from aiogram import types
from filters import Rights, is_verified
from messages import strings


@dp.message_handler(is_verified(), Rights(), Text(equals="Kategoriyalar"), state="*")
async def categories(message: types.Message, state: FSMContext):
    await state.reset_state()
    await message.answer(
        text=strings['category_request'],
        reply_markup=await categories_waiter(data=await get_categories())
    )