from aiogram import types
from callback_datas import cb_waiter


async def categories_waiter(data: list) -> types.InlineKeyboardMarkup:
    category = types.InlineKeyboardMarkup(row_width=1)
    for item in data:
        category.insert(types.InlineKeyboardButton(text=item['title'], callback_data=cb_waiter.new(id=item['id'], filter="waiter")))
    return category
