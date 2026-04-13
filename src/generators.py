from typing import Any, Dict, Iterator, List


def filter_by_currency(transactions: List[Dict[str, Any]], currency: str) -> Iterator[Dict[str, Any]]:
    """
    Фильтрует транзакции по заданной валюте и возвращает итератор.

    """
    for transaction in transactions:
        try:
            # Получаем валюту операции, обращаясь к вложенному словарю
            transaction_currency = transaction.get("operationAmount", {}).get("currency")

            # Если валюта совпадает с искомой, выдаём транзакцию
            if transaction_currency == currency:
                yield transaction
        except AttributeError:
            # Если структура словаря не соответствует ожидаемой, пропускаем транзакцию
            continue


transactions = [
    {"id": 1, "operationAmount": {"amount": "100.00", "currency": "USD"}},
    {"id": 2, "operationAmount": {"amount": "250.50", "currency": "EUR"}},
    {"id": 3, "operationAmount": {"amount": "75.00", "currency": "USD"}},
    {"id": 4, "operationAmount": {"amount": "50.00", "currency": "RUB"}},
]

# Создаём итератор
usd_transactions = filter_by_currency(transactions, "USD")

# Выводим транзакции одну за другой
for transaction in usd_transactions:
    print(transaction)


def transaction_descriptions(transactions: List[Dict[str, Any]]) -> Iterator[str]:
    """
    Принимает список словарей с транзакциями и возвращает описание каждой операции по очереди.

    """
    for transaction in transactions:

        description = transaction.get("description", "")
        yield description


transactions = [
    {"id": 1, "description": "Перевод другу", "amount": 500},
    {"id": 2, "description": "Покупка продуктов", "amount": 1500},
    {"id": 3, "description": "Оплата интернета", "amount": 800},
    {"id": 4, "amount": 300},  # У этой транзакции нет описания
]

# Создаём генератор
descriptions = transaction_descriptions(transactions)

# Получаем описания по одному через next()
print(next(descriptions))
print(next(descriptions))
print(next(descriptions))
print(next(descriptions))


def card_number_generator(start: int, end: int) -> Iterator[str]:
    """
    Генерирует номера банковских карт в заданном диапазоне.

    """
    for number in range(start, end + 1):
        # Преобразуем число в строку с ведущими нулями до 16 цифр
        card_number_str = str(number).zfill(16)

        # Разбиваем на группы по 4 цифры и объединяем пробелами
        formatted_card = " ".join(card_number_str[i : i + 4] for i in range(0, 16, 4))

        yield formatted_card


print("Первые 5 номеров карт:")
for card in card_number_generator(1, 5):
    print(card)

print("\n" + "-" * 30 + "\n")

# Пример 2: генерация номеров с 9999999999999995 по 9999999999999999
print("Последние 5 номеров карт:")
for card in card_number_generator(9999999999999995, 9999999999999999):
    print(card)

print("\n" + "-" * 30 + "\n")

# Пример 3: ручное использование через next()
gen = card_number_generator(1, 3)
print(next(gen))
print(next(gen))
print(next(gen))
