from aiogram.fsm.state import State, StatesGroup    

class AddMedicineState(StatesGroup):
    trade_name = State()
    mnn = State()
    manufacturer = State()
    form = State()
    registration_number = State()
    state = State()
    dispensing_mode = State()
    farm_group = State()
    code_atx = State()

