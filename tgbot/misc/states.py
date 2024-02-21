from aiogram.fsm.state import StatesGroup, State


class SoftwareChoice(StatesGroup):
    software = State()


class Tickets(StatesGroup):
    error_message = State()
    feature_message = State()
