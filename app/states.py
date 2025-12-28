from aiogram.fsm.state import StatesGroup, State

class AddFileState(StatesGroup):
    waiting_file = State()
