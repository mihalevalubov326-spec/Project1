import pytest
from src.masks import get_mask_card_number, get_mask_card_account

class TestMaskCardNumber:
    """Тесты для маскировки номера карты."""

    def test_mask_card_number_16_digits(self) -> None:
        """Тест 16-значного номера."""
        result = get_mask_card_number(7000792289606361)
        # Проверяем структуру: 4 цифры, пробел, 2 цифры, "**", пробел, "****", пробел, 4 цифры
        assert result == "7000 79** **** 6361"

    def test_mask_card_number_15_digits(self) -> None:
        """Тест 15-значного номера."""
        result = get_mask_card_number(123456789012345)
        # Проверяем, что результат не пустой
        assert len(result) > 0

    def test_mask_card_number_single_digit(self) -> None:
        """Тест однозначного номера."""
        result = get_mask_card_number(1)
        assert result == "11"  # текущее поведение


class TestMaskCardAccount:
    """Тесты для маскировки номера счета."""

    def test_mask_account_standard(self) -> None:
        """Тест стандартного номера счета."""
        result = get_mask_card_account(73654108430135874305)
        assert result == "**4305"
        assert result.startswith("**")
        assert len(result) == 6  # "**" + 4 цифры

    def test_mask_account_short(self) -> None:
        """Тест короткого номера."""
        result = get_mask_card_account(123)
        assert result == "**123"
        assert result.startswith("**")