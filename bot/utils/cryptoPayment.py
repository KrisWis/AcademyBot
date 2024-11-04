from aiocryptopay import AioCryptoPay
import os


# Функция для конвертации суммы конкретной валюты в USD
async def get_crypto_bot_sum(summa: float, currency: str):
    cryptopay = AioCryptoPay(os.getenv("CRYPTOPAY_API"))

    courses = await cryptopay.get_exchange_rates()

    await cryptopay.close()

    for course in courses:
        if course.source == currency and course.target == 'RUB':
            return round(float(summa / course.rate), 2)
        

# Функция для проверки того, что оплата прошла успешно
async def check_crypto_bot_invoice(invoice_id: int):
    cryptopay = AioCryptoPay(os.getenv("CRYPTOPAY_API"))

    invoice = await cryptopay.get_invoices(invoice_ids=invoice_id)
    await cryptopay.close()

    if invoice.status == 'paid':
        return True

    return False


# Функция для совершения оплаты через cryptobot
async def create_crypto_bot_invoice(summa: float, currency: str):
    crypto_bot = AioCryptoPay(os.getenv("CRYPTOPAY_API"))

    amount = await get_crypto_bot_sum(summa, currency)
    invoice = await crypto_bot.create_invoice(
        asset=currency,
        amount=amount
    )
    await crypto_bot.close()

    return invoice