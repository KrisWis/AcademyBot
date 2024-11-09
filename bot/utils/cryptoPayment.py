from aiocryptopay import AioCryptoPay, Networks
import os

# cryptopay = AioCryptoPay(os.getenv("CRYPTOPAY_API"), network=Networks.MAIN_NET)
cryptopay = AioCryptoPay(os.getenv("TEST_CRYPTOPAY_API"), network=Networks.TEST_NET)

# Функция для конвертации суммы конкретной валюты в USD
async def get_crypto_bot_sum(summa: float, currency: str):
    courses = await cryptopay.get_exchange_rates()

    await cryptopay.close()

    for course in courses:
        if course.source == currency and course.target == 'RUB':
            return round(float(summa / course.rate), 2)


# Функция для совершения оплаты
async def create_crypto_bot_invoice(summa: float, currency: str):
    amount = await get_crypto_bot_sum(1, currency)
    invoice = await cryptopay.create_invoice(
        asset=currency,
        amount=amount
    )
    await cryptopay.close()

    return invoice


# Функция для проверки того, что оплата прошла успешно
async def check_crypto_bot_invoice(invoice_id: int):
    invoice = await cryptopay.get_invoices(invoice_ids=invoice_id)
    await cryptopay.close()

    if invoice.status == 'paid':
        return True

    return False


# Функция для обработки вывода средств
async def create_crypto_bot_check(summa: float):
    check = await cryptopay.create_check(asset='USDT', amount=0.04)

    return check


# Функция получения чека по его id при выводе
async def get_check_info(check_id: int):
    check_info = await cryptopay.get_checks(asset='USDT', check_ids=check_id, count=1)

    return check_info