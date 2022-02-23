from aiogram import types
from aiogram.dispatcher.filters import CommandStart

from funcs import db, funcs
from loader import dp
from messages import strings, rights


@dp.message_handler(CommandStart())
async def on_start(message: types.Message):
    data: dict = await funcs.verify_user(user_id=message.from_user.id)
    if data:
        keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        for item in rights[data.get('role')]:
            keyboard.insert(types.KeyboardButton(text=item))
        if await db.check_user(user_id=message.from_user.id) is False:
            await db.new_user(user_id=message.from_user.id, rights=rights[data.get('role')], verified=True, identification=data.get("id"))
        else:
            await db.update_user(user_id=message.from_user.id, rights=rights[data.get('role')], verified=True, identification=data.get("id"))
        await message.answer(
            text=strings['welcome'].format(data.get('get_full_name')),
            reply_markup=keyboard
        )
    elif data is False:
        await message.answer(
            text=strings['not_verified']
        )
