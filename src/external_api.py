import os
from typing import Any, Dict, Optional

import requests
from dotenv import load_dotenv

# Загружаем переменные из .env
load_dotenv()

# Берём ключ из переменной окружения
API_KEY = os.getenv("EXCHANGE_RATES_API_KEY")
BASE_URL = "https://api.apilayer.com/exchangerates_data"


def get_exchange_rate(from_currency: str, to_currency: str = "RUB") -> Optional[float]:
    """
    Получает курс обмена через API.
    """
    if not API_KEY:
        print("API ключ не найден. Установите EXCHANGE_RATES_API_KEY в .env")
        return None

    url = f"{BASE_URL}/latest"
    params = {"base": from_currency, "symbols": to_currency}
    headers = {"apikey": API_KEY}

    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)

        if response.status_code != 200:
            print(f"Ошибка API: статус {response.status_code}, ответ: {response.text}")
            return None

        data = response.json()
        rate = data.get("rates", {}).get(to_currency)

        if rate is None:
            print(f"Не найден курс для {from_currency} -> {to_currency}")
            return None

        return float(rate)

    except requests.RequestException as e:
        print(f"Ошибка при запросе к API: {e}")
        return None


def convert_operation_to_rub(operation: Dict[str, Any]) -> float:
    """
    Конвертирует сумму операции в рубли.
    """
    try:
        operation_amount = operation.get("operationAmount")
        if operation_amount is None:
            print("В транзакции отсутствует поле operationAmount")
            return 0.0

        amount_str = operation_amount.get("amount")
        currency_info = operation_amount.get("currency", {})

        if amount_str is None:
            print("В operationAmount отсутствует поле amount")
            return 0.0

        amount = float(amount_str)
        currency = currency_info.get("code", "RUB").upper()

        if currency == "RUB":
            return round(amount, 2)

        if currency in ("USD", "EUR"):
            rate = get_exchange_rate(currency)
            if rate is not None:
                return round(amount * rate, 2)
            else:
                print(f"Не удалось конвертировать {currency} в RUB, используется 0")
                return 0.0
        else:
            print(f"Валюта {currency} не поддерживается для конвертации")
            return 0.0

    except (ValueError, TypeError, AttributeError) as e:
        print(f"Ошибка при обработке операции: {e}")
        return 0.0


# Блок для ручного тестирования (вне функций!)
if __name__ == "__main__":
    # Проверяем курс USD
    rate = get_exchange_rate("USD")
    print(f"Курс USD: {rate}")

    # Проверяем конвертацию
    test_operation = {"operationAmount": {"amount": "100", "currency": {"code": "USD"}}}
    result = convert_operation_to_rub(test_operation)
    print(f"100 USD в рублях: {result}")
