import pytest
from src.masks import get_mask_card_number, get_mask_card_account

class TestMaskCardNumber:
    """Тесты для маскировки номера карты."""

    def test_mask_card_number_standard(self):
        """Тест стандартного 16-значного номера."""
        result = get_mask_card_number("7000792289606361")
        assert result == "7000 79** **** 6361"

    def test_mask_card_number_with_int(self):
        """Тест с передачей числа."""
        result = get_mask_card_number(7000792289606361)
        assert result == "7000 79** **** 6361"

    def test_mask_card_number_empty(self):
        """Тест с пустой строкой."""
        result = get_mask_card_number("")
        print(f"Результат: '{result}'")
