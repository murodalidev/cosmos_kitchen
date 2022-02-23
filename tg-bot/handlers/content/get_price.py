from aiogram import types
from aiogram.dispatcher import FSMContext

from funcs import create_storage
from loader import dp
from messages import strings
from states import count_supplier


@dp.message_handler(content_types="text", state=count_supplier.price)
async def get_price(message: types.Message, state: FSMContext):
    price = message.text
    if price.isdigit():
        product_id = int((await state.get_data()).get("product_id"))
        category_id = int((await state.get_data()).get("category_id"))
        count = int((await state.get_data()).get("count"))
        if await create_storage(
                user_id=message.from_user.id,
                category_id=category_id,
                product_id=product_id,
                quantity=count,
                price=int(price)
        ):
            await message.answer(
                text=strings['add_storage']
            )
            await state.reset_state()
        else:
            await message.answer(
                text=strings['error']
            )
    else:
        await message.answer(
            text=strings['digits_error']
        )
