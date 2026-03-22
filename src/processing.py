def filter_by_state(transactions: list[dict], state: str = 'EXECUTED') -> list[dict]:
    """Фильтрует список транзакций по значению ключа state. Возвращает отфильтрованный список словарей"""

    filtered_list = []

    for transaction in transactions:
        transaction_state = transaction.get('state')

        if transaction_state == state:
            filtered_list.append(transaction)

    return filtered_list

transactions = [
    {'id': 1, 'state': 'EXECUTED', 'amount': 100},
    {'id': 2, 'state': 'CANCELED', 'amount': 200},
    {'id': 3, 'state': 'EXECUTED', 'amount': 300},
]

result = filter_by_state(transactions)
print(result)

def sort_by_date(transactions: list[dict], descending: bool = True) -> list[dict]:
    """Сортирует транзакции по дате."""

    return sorted(transactions, key=lambda x: x.get('date', ''), reverse=descending)

transactions_with_dates = [
    {'id': 1, 'state': 'EXECUTED', 'amount': 100, 'date': '2024-03-15'},
    {'id': 2, 'state': 'CANCELED', 'amount': 200, 'date': '2024-01-10'},
    {'id': 3, 'state': 'EXECUTED', 'amount': 300, 'date': '2024-02-20'},
]

sorted_result = sort_by_date(transactions)
print(sorted_result)
