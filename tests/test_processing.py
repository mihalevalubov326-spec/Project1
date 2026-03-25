import pytest
from src.processing import filter_by_state, sort_by_date


class TestFilterByState:
    """Тесты для фильтрации по state."""

    @pytest.fixture
    def sample_transactions(self):
        """Фикстура с тестовыми данными."""
        return [
            {'id': 1, 'state': 'EXECUTED', 'amount': 100},
            {'id': 2, 'state': 'CANCELED', 'amount': 200},
            {'id': 3, 'state': 'EXECUTED', 'amount': 300},
            {'id': 4, 'state': 'PENDING', 'amount': 400},
        ]

    def test_filter_by_state_default(self, sample_transactions):
        """Тест фильтрации по умолчанию (EXECUTED)."""
        result = filter_by_state(sample_transactions)
        assert len(result) == 2
        assert all(t['state'] == 'EXECUTED' for t in result)

    def test_filter_by_state_canceled(self, sample_transactions):
        """Тест фильтрации по CANCELED."""
        result = filter_by_state(sample_transactions, 'CANCELED')
        assert len(result) == 1
        assert result[0]['state'] == 'CANCELED'

    def test_filter_by_state_not_found(self, sample_transactions):
        """Тест фильтрации с несуществующим значением."""
        result = filter_by_state(sample_transactions, 'NOT_EXISTS')
        assert result == []

    def test_filter_by_state_empty_list(self):
        """Тест с пустым списком."""
        result = filter_by_state([])
        assert result == []


class TestSortByDate:
    """Тесты для сортировки по дате."""

    @pytest.fixture
    def sample_transactions_with_dates(self):
        """Фикстура с тестовыми данными, содержащими даты."""
        return [
            {'id': 1, 'date': '2024-03-15', 'amount': 100},
            {'id': 2, 'date': '2024-01-10', 'amount': 200},
            {'id': 3, 'date': '2024-02-20', 'amount': 300},
            {'id': 4, 'date': '2024-04-05', 'amount': 400},
        ]

    def test_sort_by_date_descending(self, sample_transactions_with_dates):
        """Тест сортировки по убыванию (новые → старые)."""
        result = sort_by_date(sample_transactions_with_dates)
        dates = [t['date'] for t in result]
        assert dates == ['2024-04-05', '2024-03-15', '2024-02-20', '2024-01-10']

    def test_sort_by_date_ascending(self, sample_transactions_with_dates):
        """Тест сортировки по возрастанию (старые → новые)."""
        result = sort_by_date(sample_transactions_with_dates, descending=False)
        dates = [t['date'] for t in result]
        assert dates == ['2024-01-10', '2024-02-20', '2024-03-15', '2024-04-05']

    def test_sort_by_date_missing_date(self):
        """Тест с отсутствующими датами."""
        transactions = [
            {'id': 1, 'amount': 100},  # нет даты
            {'id': 2, 'date': '2024-01-10', 'amount': 200},
        ]
        result = sort_by_date(transactions)
        # Элементы без даты должны быть в конце
        assert result[0]['id'] == 2
        assert result[1]['id'] == 1

    def test_sort_by_date_empty_list(self):
        """Тест с пустым списком."""
        result = sort_by_date([])
        assert result == []
