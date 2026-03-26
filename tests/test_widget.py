import pytest
from src.widget import mask_account_card, get_date


class TestMaskAccountCard:
    """Тесты для маскировки карты/счета."""

    @pytest.mark.parametrize(
        "input_str,expected",
        [
            ("Maestro 7000792289606361", "Maestro 7000 79** **** 6361"),
            ("Visa Platinum 7000792289606361", "Visa Platinum 7000 79** **** 6361"),
            ("MasterCard 7000792289606361", "MasterCard 7000 79** **** 6361"),
            ("American Express 7000792289606361", "American Express 7000 79** **** 6361"),
        ],
    )
    def test_mask_card(self, input_str: str, expected: str) -> None:
        """Параметризованный тест маскировки карт."""
        result = mask_account_card(input_str)
        assert result == expected

    @pytest.mark.parametrize(
        "input_str,expected",
        [
            ("Счет 73654108430135874305", "Счет **4305"),
            ("Счет 12345678901234567890", "Счет **7890"),
            ("Счет 1000000000000000", "Счет **0000"),
            ("Счет 12345", "Счет **2345"),
            ("Счет 123", "Счет 123"),  # исправлено: короткий счет не маскируется
            ("Счет 1", "Счет 1"),  # исправлено: короткий счет не маскируется
        ],
    )
    def test_mask_account(self, input_str: str, expected: str) -> None:
        """Параметризованный тест маскировки счетов."""
        result = mask_account_card(input_str)
        assert result == expected

    @pytest.mark.parametrize(
        "input_str,expected",
        [
            ("Visa 12345", "Visa 12345"),
            ("Maestro 123", "Maestro 123"),
            ("Счет 12", "Счет 12"),
            ("Visa 1", "Visa 1"),
        ],
    )
    def test_mask_card_invalid_length(self, input_str: str, expected: str) -> None:
        """Тест с некорректной длиной номера."""
        result = mask_account_card(input_str)
        assert result == expected

    @pytest.mark.parametrize(
        "input_str,expected",
        [
            ("Visa7000792289606361", "Visa7000792289606361"),
            ("Maestro7000792289606361", "Maestro7000792289606361"),
            ("Счет73654108430135874305", "Счет73654108430135874305"),
        ],
    )
    def test_mask_card_no_space(self, input_str: str, expected: str) -> None:
        """Тест без пробела."""
        result = mask_account_card(input_str)
        assert result == expected


class TestGetDate:
    """Тесты для преобразования даты."""

    @pytest.mark.parametrize(
        "input_str,expected",
        [
            ("2024-03-11T02:26:18.671407", "11.03.2024"),
            ("2024-12-31T23:59:59", "31.12.2024"),
            ("2025-01-01T00:00:00", "01.01.2025"),
            ("2024-02-29T12:00:00", "29.02.2024"),
            ("2023-02-28T12:00:00", "28.02.2023"),
            ("2024-01-01T00:00:00.123456", "01.01.2024"),
        ],
    )
    def test_get_date(self, input_str: str, expected: str) -> None:
        """Параметризованный тест преобразования даты."""
        result = get_date(input_str)
        assert result == expected
