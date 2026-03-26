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

    @pytest.mark.parametrize(
        "state,expected_ids",
        [
            ("EXECUTED", [1, 3]),
            ("CANCELED", [2]),
            ("PENDING", [4]),
            ("NOT_EXISTS", []),
        ],
    )
    def test_filter_by_state(
        self, sample_transactions: List[Dict[str, Any]], state: str, expected_ids: List[int]
    ) -> None:
        """Параметризованный тест фильтрации по state."""
        result = filter_by_state(sample_transactions, state)
        assert [t["id"] for t in result] == expected_ids
        if expected_ids:
            assert all(t["state"] == state for t in result)

    def test_filter_by_state_empty_list(self) -> None:
        """Тест с пустым списком."""
        result = filter_by_state([])
        assert result == []

    @pytest.mark.parametrize(
        "transactions,expected_ids",
        [
            ([{"id": 1, "amount": 100}, {"id": 2, "state": "EXECUTED", "amount": 200}], [2]),
            ([{"id": 1, "state": "CANCELED", "amount": 100}, {"id": 2, "amount": 200}], []),
            ([{"id": 1, "amount": 100}, {"id": 2, "amount": 200}], []),
        ],
    )
    def test_filter_by_state_missing_state_key(
        self, transactions: List[Dict[str, Any]], expected_ids: List[int]
    ) -> None:
        """Тест с транзакциями, у которых нет ключа state."""
        result = filter_by_state(transactions)
        assert [t["id"] for t in result] == expected_ids


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

    @pytest.mark.parametrize(
        "descending,expected_dates,expected_ids",
        [
            (True, ["2024-04-05", "2024-03-15", "2024-02-20", "2024-01-10"], [4, 1, 3, 2]),
            (False, ["2024-01-10", "2024-02-20", "2024-03-15", "2024-04-05"], [2, 3, 1, 4]),
        ],
    )
    def test_sort_by_date(
        self,
        sample_transactions_with_dates: List[Dict[str, Any]],
        descending: bool,
        expected_dates: List[str],
        expected_ids: List[int],
    ) -> None:
        """Параметризованный тест сортировки по дате."""
        result = sort_by_date(sample_transactions_with_dates, descending=descending)
        assert [t["date"] for t in result] == expected_dates
        assert [t["id"] for t in result] == expected_ids

    @pytest.mark.parametrize(
        "transactions,expected_ids",
        [
            (
                [
                    {"id": 1, "amount": 100},
                    {"id": 2, "date": "2024-01-10", "amount": 200},
                    {"id": 3, "date": "2024-03-15", "amount": 300},
                    {"id": 4, "amount": 400},
                ],
                [3, 2, 1, 4],  # исправлено: [3, 2, 1, 4] вместо [2, 3, 1, 4]
            ),
            (
                [
                    {"id": 1, "amount": 100},
                    {"id": 2, "date": "2024-01-10", "amount": 200},
                ],
                [2, 1],
            ),
            (
                [
                    {"id": 1, "amount": 100},
                    {"id": 2, "amount": 200},
                ],
                [1, 2],
            ),
        ],
    )
    def test_sort_by_date_with_missing_dates(
        self, transactions: List[Dict[str, Any]], expected_ids: List[int]
    ) -> None:
        """Тест с транзакциями, у которых отсутствует дата."""
        result = sort_by_date(transactions)
        assert [t["id"] for t in result] == expected_ids

    @pytest.mark.parametrize(
        "transactions,expected_ids",
        [
            ([{"id": 1, "date": "2024-01-10", "amount": 100}], [1]),
            ([{"id": 1, "date": "2024-01-10", "amount": 100}, {"id": 2, "date": "2024-01-10", "amount": 200}], [1, 2]),
            (
                [
                    {"id": 3, "date": "2024-01-10", "amount": 300},
                    {"id": 1, "date": "2024-01-10", "amount": 100},
                    {"id": 2, "date": "2024-01-10", "amount": 200},
                ],
                [3, 1, 2],
            ),
        ],
    )
    def test_sort_by_date_single_and_same_dates(
        self, transactions: List[Dict[str, Any]], expected_ids: List[int]
    ) -> None:
        """Тест с одной транзакцией и с одинаковыми датами."""
        result = sort_by_date(transactions)
        assert [t["id"] for t in result] == expected_ids

    def test_sort_by_date_empty_list(self) -> None:
        """Тест с пустым списком."""
        result = sort_by_date([])
        assert result == []
