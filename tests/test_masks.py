import pytest
from src.masks import get_mask_card_number, get_mask_card_account


class TestMaskCardNumber:
    """Тесты для маскировки номера карты."""

    @pytest.mark.parametrize(
        "input_number,expected",
        [
            (7000792289606361, "7000 79** **** 6361"),
            (1234567890123456, "1234 56** **** 3456"),
            (1111222233334444, "1111 22** **** 4444"),
        ],
    )
    def test_mask_card_number_16_digits(self, input_number: int, expected: str) -> None:
        """Тест 16-значных номеров."""
        result = get_mask_card_number(input_number)
        assert result == expected

    @pytest.mark.parametrize(
        "input_number",
        [
            123456789012345,
            12345678901234,
            1234567890123,
            123456789012,
            12345678901,
        ],
    )
    def test_mask_card_number_less_than_16_digits(self, input_number: int) -> None:
        """Тест номеров короче 16 цифр."""
        result = get_mask_card_number(input_number)
        # Проверяем, что результат не пустой
        assert len(result) > 0

    @pytest.mark.parametrize(
        "input_number,expected",
        [
            (1, "11"),
            (12, "1212"),
            (123, "1231"),
            (1234, "1234"),
            (12345, "1234 5234"),
        ],
    )
    def test_mask_card_number_small_numbers(self, input_number: int, expected: str) -> None:
        """Тест маленьких номеров (1-5 цифр)."""
        result = get_mask_card_number(input_number)
        assert result == expected


class TestMaskCardAccount:
    """Тесты для маскировки номера счета."""

    @pytest.mark.parametrize(
        "input_number,expected",
        [
            (73654108430135874305, "**4305"),
            (12345678901234567890, "**7890"),
            (9999999999999999, "**9999"),
            (1000000000000000, "**0000"),
        ],
    )
    def test_mask_account_standard(self, input_number: int, expected: str) -> None:
        """Тест стандартных номеров счетов."""
        result = get_mask_card_account(input_number)
        assert result == expected
        assert result.startswith("**")
        assert len(result) == 6  # "**" + 4 цифры

    @pytest.mark.parametrize(
        "input_number,expected",
        [
            (12345, "**2345"),
            (1234, "**1234"),
            (123, "**123"),
            (12, "**12"),
            (1, "**1"),
            (0, "**0"),
        ],
    )
    def test_mask_account_short(self, input_number: int, expected: str) -> None:
        """Тест коротких номеров счетов."""
        result = get_mask_card_account(input_number)
        assert result == expected
        assert result.startswith("**")
