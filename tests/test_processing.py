import pytest
from typing import List, Dict, Any
from src.processing import filter_by_state, sort_by_date


class TestFilterByState:
    """Тесты для фильтрации транзакций по state."""

    @pytest.fixture
    def sample_transactions(self) -> List[Dict[str, Any]]:
        """Фикстура с тестовыми данными."""
        return [
            {"id": 1, "state": "EXECUTED", "amount": 100},
            {"id": 2, "state": "CANCELED", "amount": 200},
            {"id": 3, "state": "EXECUTED", "amount": 300},
            {"id": 4, "state": "PENDING", "amount": 400},
        ]

    def test_filter_by_state_default(self, sample_transactions: List[Dict[str, Any]]) -> None:
        """Тест фильтрации по умолчанию (state='EXECUTED')."""
        result = filter_by_state(sample_transactions)
        assert len(result) == 2
        assert all(t["state"] == "EXECUTED" for t in result)
        assert [t["id"] for t in result] == [1, 3]

    def test_filter_by_state_canceled(self, sample_transactions: List[Dict[str, Any]]) -> None:
        """Тест фильтрации по state='CANCELED'."""
        result = filter_by_state(sample_transactions, "CANCELED")
        assert len(result) == 1
        assert result[0]["state"] == "CANCELED"
        assert result[0]["id"] == 2

    def test_filter_by_state_pending(self, sample_transactions: List[Dict[str, Any]]) -> None:
        """Тест фильтрации по state='PENDING'."""
        result = filter_by_state(sample_transactions, "PENDING")
        assert len(result) == 1
        assert result[0]["state"] == "PENDING"
        assert result[0]["id"] == 4

    def test_filter_by_state_not_found(self, sample_transactions: List[Dict[str, Any]]) -> None:
        """Тест фильтрации с несуществующим значением."""
        result = filter_by_state(sample_transactions, "NOT_EXISTS")
        assert result == []

    def test_filter_by_state_empty_list(self) -> None:
        """Тест с пустым списком."""
        result = filter_by_state([])
        assert result == []

    def test_filter_by_state_missing_state_key(self) -> None:
        """Тест с транзакцией, у которой нет ключа state."""
        transactions: List[Dict[str, Any]] = [
            {"id": 1, "amount": 100},  # нет ключа state
            {"id": 2, "state": "EXECUTED", "amount": 200},
        ]
        result = filter_by_state(transactions)
        assert len(result) == 1
        assert result[0]["id"] == 2


class TestSortByDate:
    """Тесты для сортировки транзакций по дате."""

    @pytest.fixture
    def sample_transactions_with_dates(self) -> List[Dict[str, Any]]:
        """Фикстура с тестовыми данными, содержащими даты."""
        return [
            {"id": 1, "date": "2024-03-15", "amount": 100},
            {"id": 2, "date": "2024-01-10", "amount": 200},
            {"id": 3, "date": "2024-02-20", "amount": 300},
            {"id": 4, "date": "2024-04-05", "amount": 400},
        ]

    def test_sort_by_date_descending(self, sample_transactions_with_dates: List[Dict[str, Any]]) -> None:
        """Тест сортировки по убыванию (новые → старые)."""
        result = sort_by_date(sample_transactions_with_dates)
        expected_dates = ["2024-04-05", "2024-03-15", "2024-02-20", "2024-01-10"]
        assert [t["date"] for t in result] == expected_dates
        assert [t["id"] for t in result] == [4, 1, 3, 2]

    def test_sort_by_date_ascending(self, sample_transactions_with_dates: List[Dict[str, Any]]) -> None:
        """Тест сортировки по возрастанию (старые → новые)."""
        result = sort_by_date(sample_transactions_with_dates, descending=False)
        expected_dates = ["2024-01-10", "2024-02-20", "2024-03-15", "2024-04-05"]
        assert [t["date"] for t in result] == expected_dates
        assert [t["id"] for t in result] == [2, 3, 1, 4]

    def test_sort_by_date_with_missing_dates(self) -> None:
        """Тест с транзакциями, у которых отсутствует дата."""
        transactions: List[Dict[str, Any]] = [
            {"id": 1, "amount": 100},  # нет даты
            {"id": 2, "date": "2024-01-10", "amount": 200},
            {"id": 3, "date": "2024-03-15", "amount": 300},
            {"id": 4, "amount": 400},  # нет даты
        ]
        result = sort_by_date(transactions)
        # Элементы без даты должны быть в конце
        assert [t["id"] for t in result] == [2, 3, 1, 4]

    def test_sort_by_date_single_transaction(self) -> None:
        """Тест с одной транзакцией."""
        transactions: List[Dict[str, Any]] = [{"id": 1, "date": "2024-01-10", "amount": 100}]
        result = sort_by_date(transactions)
        assert len(result) == 1
        assert result[0]["id"] == 1

    def test_sort_by_date_empty_list(self) -> None:
        """Тест с пустым списком."""
        result = sort_by_date([])
        assert result == []

    def test_sort_by_date_same_dates(self) -> None:
        """Тест с одинаковыми датами."""
        transactions: List[Dict[str, Any]] = [
            {"id": 1, "date": "2024-01-10", "amount": 100},
            {"id": 2, "date": "2024-01-10", "amount": 200},
            {"id": 3, "date": "2024-01-10", "amount": 300},
        ]
        result = sort_by_date(transactions)
        assert len(result) == 3
        # Порядок при одинаковых датах сохраняется
        assert [t["id"] for t in result] == [1, 2, 3]