from aiogram.fsm.state import StatesGroup, State


class Form(StatesGroup):
    menu = State()
    operation = State()
    period = State()
