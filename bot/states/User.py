from aiogram.fsm.state import State, StatesGroup

# Состояния при нажатии кнопки "Профиль"
class ProfileStates(StatesGroup):
    choose_sumOfPayment = State()
    choose_sumOfWithdraw = State()
    write_cardNumber = State()


# Состояния при нажатии кнопки "Поддержка"
class SupportStates(StatesGroup):
    write_text_of_supportTicket = State()

    