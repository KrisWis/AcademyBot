from aiogram.fsm.state import State, StatesGroup


# Состояния при ответе на тикет поддержки
class SupportAgentStates(StatesGroup):
    write_text_for_answer = State()

    