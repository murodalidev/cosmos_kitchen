from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

from funcs import check_rights, verify


class is_verified(BoundFilter):
    async def check(self, message: types.Message) -> bool:
        if await verify(user_id=message.from_user.id) is False:
            return False
        else:
            return True


class Rights(BoundFilter):
    async def check(self, message: types.Message) -> bool:
        if message.text not in await check_rights(user_id=message.from_user.id):
            return False
        else:
            return True

