from aiogram.fsm.state import State, StatesGroup


# Состояния для панели руководителя
class LeaderMenuStates(StatesGroup):
    write_supportTicket_id = State()

    