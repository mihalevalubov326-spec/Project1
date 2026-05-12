import os
from typing import Any, Dict, Optional

import requests
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

API_KEY = os.getenv("EXCHANGE_RATES_API_KEY")
BASE_URL = "https://api.apilayer.com/exchangerates_data"


def get_exchange_rate(from_currency: str, to_currency: str = "RUB") -> Optional[float]:
    """
    Получает курс обмена через API.

    Аргументы:
        from_currency (str): Исходная валюта (USD, EUR).
        to_currency (str): Целевая валюта (по умолчанию RUB).

    Возвращает:
        Optional[float]: Курс обмена или None при ошибке.
    """
    if not API_KEY:
        print("API ключ не найден. Установите EXCHANGE_RATES_API_KEY в .env")
        return None

    url = f"{BASE_URL}/latest"
    params = {"base": from_currency, "symbols": to_currency}
    headers = {"apikey": API_KEY}

    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)
        response.raise_for_status()

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

    Аргументы:
        operation (Dict[str, Any]): Словарь транзакции с полями amount и currency.

    Возвращает:
        float: Сумма в рублях.
    """
    try:
        amount = float(operation.get("amount", 0))
        currency = operation.get("currency", "RUB").upper()

        if currency == "RUB":
            return amount

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

    except (ValueError, TypeError) as e:
        print(f"Ошибка при обработке операции: {e}")
        return 0.0
