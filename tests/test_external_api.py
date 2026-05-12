from unittest.mock import MagicMock, patch

import pytest

from src.external_api import convert_operation_to_rub, get_exchange_rate

# ========== ТЕСТЫ ДЛЯ get_exchange_rate ==========


@patch("src.external_api.API_KEY", "fake_key")  # подменяем API ключ
@patch("src.external_api.requests.get")
def test_get_exchange_rate_success(mock_get):
    """Тест: успешное получение курса."""
    # Настраиваем мок-ответ
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"rates": {"RUB": 90.5}}
    mock_get.return_value = mock_response

    # Вызываем функцию
    rate = get_exchange_rate("USD", "RUB")

    # Проверяем результат
    assert rate == 90.5

    # Проверяем, что запрос был сделан с правильными параметрами
    mock_get.assert_called_once()

    # Дополнительная проверка: какие аргументы передавались
    call_args = mock_get.call_args
    assert call_args[1]["params"]["base"] == "USD"
    assert call_args[1]["params"]["symbols"] == "RUB"


@patch("src.external_api.requests.get")
def test_get_exchange_rate_network_error(mock_get):
    """Тест: ошибка сети."""
    mock_get.side_effect = Exception("Network error")

    rate = get_exchange_rate("USD")

    assert rate is None


@patch("src.external_api.requests.get")
def test_get_exchange_rate_no_rate(mock_get):
    """Тест: ответ API без нужной валюты."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"rates": {}}
    mock_get.return_value = mock_response

    rate = get_exchange_rate("USD")

    assert rate is None


@patch("src.external_api.requests.get")
def test_get_exchange_rate_no_api_key(mock_get):
    """Тест: отсутствует API ключ."""
    with patch("src.external_api.API_KEY", None):
        rate = get_exchange_rate("USD")
        assert rate is None
        mock_get.assert_not_called()


# ========== ТЕСТЫ ДЛЯ convert_operation_to_rub ==========


def test_convert_operation_rub():
    """Тест: конвертация рубля в рубли (без изменений)."""
    operation = {"amount": 100, "currency": "RUB"}
    result = convert_operation_to_rub(operation)
    assert result == 100.0


@patch("src.external_api.get_exchange_rate")
def test_convert_operation_usd(mock_get_rate):
    """Тест: конвертация USD в RUB."""
    mock_get_rate.return_value = 90.5
    operation = {"amount": 10, "currency": "USD"}

    result = convert_operation_to_rub(operation)

    assert result == 905.0
    mock_get_rate.assert_called_once_with("USD")


@patch("src.external_api.get_exchange_rate")
def test_convert_operation_eur(mock_get_rate):
    """Тест: конвертация EUR в RUB."""
    mock_get_rate.return_value = 98.0
    operation = {"amount": 5, "currency": "EUR"}

    result = convert_operation_to_rub(operation)

    assert result == 490.0
    mock_get_rate.assert_called_once_with("EUR")


@patch("src.external_api.get_exchange_rate")
def test_convert_operation_unsupported_currency(mock_get_rate):
    """Тест: неподдерживаемая валюта."""
    operation = {"amount": 100, "currency": "GBP"}

    result = convert_operation_to_rub(operation)

    assert result == 0.0
    mock_get_rate.assert_not_called()


def test_convert_operation_missing_amount():
    """Тест: отсутствует поле amount."""
    operation = {"currency": "USD"}
    result = convert_operation_to_rub(operation)
    assert result == 0.0


def test_convert_operation_invalid_amount():
    """Тест: нечисловое значение amount."""
    operation = {"amount": "not a number", "currency": "USD"}
    result = convert_operation_to_rub(operation)
    assert result == 0.0


@patch("src.external_api.get_exchange_rate")
def test_convert_operation_api_failure(mock_get_rate):
    """Тест: API вернул None (ошибка конвертации)."""
    mock_get_rate.return_value = None
    operation = {"amount": 10, "currency": "USD"}

    result = convert_operation_to_rub(operation)

    assert result == 0.0
