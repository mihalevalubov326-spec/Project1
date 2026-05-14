import pytest
import requests
from unittest.mock import patch, MagicMock
from src.external_api import get_exchange_rate, convert_operation_to_rub

# ========== ТЕСТЫ ДЛЯ get_exchange_rate ==========


@patch("src.external_api.API_KEY", "fake_key")
@patch("src.external_api.requests.get")
def test_get_exchange_rate_success(mock_get: MagicMock) -> None:
    """Тест: успешное получение курса."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"rates": {"RUB": 90.5}}
    mock_get.return_value = mock_response

    rate = get_exchange_rate("USD", "RUB")

    assert rate == 90.5
    mock_get.assert_called_once()


@patch("src.external_api.API_KEY", "fake_key")
@patch("src.external_api.requests.get")
def test_get_exchange_rate_network_error(mock_get: MagicMock) -> None:
    """Тест: ошибка сети."""
    # Используем requests.RequestException вместо Exception
    mock_get.side_effect = requests.RequestException("Network error")

    rate = get_exchange_rate("USD")

    assert rate is None


@patch("src.external_api.API_KEY", "fake_key")
@patch("src.external_api.requests.get")
def test_get_exchange_rate_no_rate(mock_get: MagicMock) -> None:
    """Тест: ответ API без нужной валюты."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"rates": {}}
    mock_get.return_value = mock_response

    rate = get_exchange_rate("USD")

    assert rate is None


@patch("src.external_api.API_KEY", None)
def test_get_exchange_rate_no_api_key() -> None:
    """Тест: отсутствует API ключ."""
    rate = get_exchange_rate("USD")
    assert rate is None


# ========== ТЕСТЫ ДЛЯ convert_operation_to_rub ==========


def test_convert_operation_rub() -> None:
    """Тест: конвертация рубля в рубли (без изменений)."""
    operation = {"operationAmount": {"amount": "100.50", "currency": {"code": "RUB"}}}
    result = convert_operation_to_rub(operation)
    assert result == 100.5


@patch("src.external_api.get_exchange_rate")
def test_convert_operation_usd(mock_get_rate: MagicMock) -> None:
    """Тест: конвертация USD в RUB."""
    mock_get_rate.return_value = 90.5
    operation = {"operationAmount": {"amount": "10.00", "currency": {"code": "USD"}}}

    result = convert_operation_to_rub(operation)

    assert result == 905.0
    mock_get_rate.assert_called_once_with("USD")


@patch("src.external_api.get_exchange_rate")
def test_convert_operation_eur(mock_get_rate: MagicMock) -> None:
    """Тест: конвертация EUR в RUB."""
    mock_get_rate.return_value = 98.0
    operation = {"operationAmount": {"amount": "5.00", "currency": {"code": "EUR"}}}

    result = convert_operation_to_rub(operation)

    assert result == 490.0
    mock_get_rate.assert_called_once_with("EUR")


def test_convert_operation_missing_operation_amount() -> None:
    """Тест: отсутствует поле operationAmount."""
    operation = {"id": 1}
    result = convert_operation_to_rub(operation)
    assert result == 0.0


def test_convert_operation_missing_amount() -> None:
    """Тест: отсутствует поле amount в operationAmount."""
    operation = {"operationAmount": {"currency": {"code": "USD"}}}
    result = convert_operation_to_rub(operation)
    assert result == 0.0


def test_convert_operation_invalid_amount() -> None:
    """Тест: нечисловое значение amount."""
    operation = {"operationAmount": {"amount": "not a number", "currency": {"code": "USD"}}}
    result = convert_operation_to_rub(operation)
    assert result == 0.0


def test_convert_operation_unsupported_currency() -> None:
    """Тест: неподдерживаемая валюта."""
    operation = {"operationAmount": {"amount": "100", "currency": {"code": "GBP"}}}
    result = convert_operation_to_rub(operation)
    assert result == 0.0


@patch("src.external_api.get_exchange_rate")
def test_convert_operation_api_failure(mock_get_rate: MagicMock) -> None:
    """Тест: API вернул None (ошибка конвертации)."""
    mock_get_rate.return_value = None
    operation = {"operationAmount": {"amount": "10.00", "currency": {"code": "USD"}}}

    result = convert_operation_to_rub(operation)

    assert result == 0.0
