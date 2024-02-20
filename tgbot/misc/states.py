from aiogram.fsm.state import StatesGroup, State


class SoftwareChoice(StatesGroup):
    chosen_software = State()
