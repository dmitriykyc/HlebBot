from aiogram.dispatcher.filters.state import StatesGroup, State


class CreateAnswer(StatesGroup):
    get_data = State()
