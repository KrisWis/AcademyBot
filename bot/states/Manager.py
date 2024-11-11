from aiogram.fsm.state import State, StatesGroup


# Состояния для работы менеджера с рефералами
class ManagerRefStates(StatesGroup):
    write_ref_percent = State()
