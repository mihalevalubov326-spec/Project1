from src.widget import mask_account_card, get_date


class TestMaskAccountCard:
    """Тесты для маскировки карты/счета."""

    def test_mask_card_maestro(self) -> None:
        """Тест маскировки карты Maestro."""
        result = mask_account_card("Maestro 7000792289606361")
        assert result == "Maestro 7000 79** **** 6361"

    def test_mask_card_visa(self) -> None:
        """Тест маскировки карты Visa."""
        result = mask_account_card("Visa Platinum 7000792289606361")
        assert result == "Visa Platinum 7000 79** **** 6361"

    def test_mask_account(self) -> None:
        """Тест маскировки счета."""
        result = mask_account_card("Счет 73654108430135874305")
        assert result == "Счет **4305"

    def test_mask_card_invalid_length(self) -> None:
        """Тест с некорректной длиной номера."""
        result = mask_account_card("Visa 12345")
        assert result == "Visa 12345"

    def test_mask_card_no_space(self) -> None:
        """Тест без пробела."""
        result = mask_account_card("Visa7000792289606361")
        assert result == "Visa7000792289606361"


class TestGetDate:
    """Тесты для преобразования даты."""

    def test_get_date_standard(self) -> None:
        """Тест стандартного формата ISO."""
        result = get_date("2024-03-11T02:26:18.671407")
        assert result == "11.03.2024"

    def test_get_date_without_microseconds(self) -> None:
        """Тест без микросекунд."""
        result = get_date("2024-12-31T23:59:59")
        assert result == "31.12.2024"

    def test_get_date_new_year(self) -> None:
        """Тест с новогодней датой."""
        result = get_date("2025-01-01T00:00:00")
        assert result == "01.01.2025"
