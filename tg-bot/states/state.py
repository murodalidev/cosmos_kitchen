from aiogram.dispatcher.filters.state import StatesGroup, State


class count_state(StatesGroup):
    count = State()
    table = State()


class count_supplier(StatesGroup):
    count = State()
    price = State()