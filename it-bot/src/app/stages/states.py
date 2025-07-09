from aiogram.filters.state import StatesGroup, State

class RegForm(StatesGroup):
    fio = State()
    phone = State()
    car = State()

