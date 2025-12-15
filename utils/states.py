from aiogram.fsm.state import State, StatesGroup    

class AdminStates(StatesGroup):
    WAITING_FOR_EXCEL = State()
    CONFIRM_CLEAR_DATABASE = State()