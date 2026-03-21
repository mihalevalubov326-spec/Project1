def filter_by_state(transactions, state='EXECUTED'):
    """
    Фильтрует список транзакций по значению ключа state. Возвращает отфильтрованный список словарей
    """
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

def sort_by_date(transactions, descending=True):
    """Сортирует транзакции по дате."""
    return sorted(transactions, key=lambda x: x.get('date', ''), reverse=descending)

sorted_result = sort_by_date(transactions)
print(sorted_result)