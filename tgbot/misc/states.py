from aiogram.fsm.state import StatesGroup, State


class SoftwareChoice(StatesGroup):
    software = State()


class ErrorMessage(StatesGroup):
    error_message = State()

