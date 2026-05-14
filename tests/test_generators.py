from typing import Any, Dict, List

import pytest

from src.generators import card_number_generator, filter_by_currency, transaction_descriptions


@pytest.fixture
def sample_transactions() -> List[Dict[str, Any]]:
    """Фикстура с тестовыми данными для фильтрации по валюте."""
    return [
        {"operationAmount": {"currency": "USD"}},
        {"operationAmount": {"currency": "RUB"}},
        {"operationAmount": {"currency": "USD"}},
        {"operationAmount": {"currency": "EUR"}},
        {"id": 5},  # нет ключа operationAmount
        {"operationAmount": {}},  # нет ключа currency
    ]


@pytest.mark.parametrize(
    "currency, expected_count",
    [
        ("USD", 2),
        ("EUR", 1),
        ("RUB", 1),
        ("GBP", 0),
    ],
)
def test_filter_by_currency(sample_transactions: List[Dict[str, Any]], currency: str, expected_count: int) -> None:
    """Параметризованный тест: разные валюты."""
    gen = filter_by_currency(sample_transactions, currency)
    result = list(gen)
    assert len(result) == expected_count
    for item in result:
        assert item.get("operationAmount", {}).get("currency") == currency


def test_filter_by_currency_empty_list() -> None:
    """Тест: пустой список."""
    gen = filter_by_currency([], "USD")
    with pytest.raises(StopIteration):
        next(gen)


# ========== ТЕСТЫ ДЛЯ transaction_descriptions ==========


@pytest.fixture
def sample_transactions_with_descriptions() -> List[Dict[str, Any]]:
    """Фикстура с тестовыми данными для описаний транзакций."""
    return [
        {"description": "Первая транзакция"},
        {"description": "Вторая транзакция"},
        {"id": 3},  # Нет описания
        {"description": "Четвёртая транзакция"},
    ]


@pytest.mark.parametrize(
    "index, expected",
    [
        (0, "Первая транзакция"),
        (1, "Вторая транзакция"),
        (2, ""),
        (3, "Четвёртая транзакция"),
    ],
)
def test_transaction_descriptions(
    sample_transactions_with_descriptions: List[Dict[str, Any]], index: int, expected: str
) -> None:
    """Параметризованный тест: проверка каждого описания по индексу."""
    gen = transaction_descriptions(sample_transactions_with_descriptions)
    all_descriptions = list(gen)
    assert all_descriptions[index] == expected


def test_transaction_descriptions_empty_list() -> None:
    """Тест: пустой список."""
    gen = transaction_descriptions([])
    with pytest.raises(StopIteration):
        next(gen)


@pytest.mark.parametrize(
    "data, expected",
    [
        ([], []),
        ([{"description": "A"}, {"description": "B"}], ["A", "B"]),
        ([{"id": 1}, {"id": 2}], ["", ""]),
        ([{"description": "X"}, {}, {"description": "Y"}], ["X", "", "Y"]),
    ],
)
def test_transaction_descriptions_various_cases(data: List[Dict[str, Any]], expected: List[str]) -> None:
    """Параметризованный тест: разные наборы данных."""
    gen = transaction_descriptions(data)
    assert list(gen) == expected


# ========== ТЕСТЫ ДЛЯ card_number_generator ==========


@pytest.mark.parametrize(
    "start, end, expected",
    [
        (1, 1, ["0000 0000 0000 0001"]),
        (1, 3, ["0000 0000 0000 0001", "0000 0000 0000 0002", "0000 0000 0000 0003"]),
        (42, 42, ["0000 0000 0000 0042"]),
        (
            9999,
            10002,
            [
                "0000 0000 0000 9999",
                "0000 0000 0001 0000",
                "0000 0000 0001 0001",
                "0000 0000 0001 0002",
            ],
        ),
        (
            9999999999999995,
            9999999999999999,
            [
                "9999 9999 9999 9995",
                "9999 9999 9999 9996",
                "9999 9999 9999 9997",
                "9999 9999 9999 9998",
                "9999 9999 9999 9999",
            ],
        ),
    ],
)
def test_card_number_generator(start: int, end: int, expected: List[str]) -> None:
    """Параметризованный тест: разные диапазоны."""
    gen = card_number_generator(start, end)
    assert list(gen) == expected


def test_card_number_generator_empty_range() -> None:
    """Тест: пустой диапазон (start > end)."""
    gen = card_number_generator(10, 5)
    with pytest.raises(StopIteration):
        next(gen)
