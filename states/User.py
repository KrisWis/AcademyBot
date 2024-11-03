from aiogram.fsm.state import State, StatesGroup

class ProfileStates(StatesGroup):
    choose_sumOfPayment = State()
    choose_sumOfWithdraw = State()
    write_cardNumber = State()