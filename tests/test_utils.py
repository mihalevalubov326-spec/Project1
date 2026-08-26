import json
from pathlib import Path
from typing import Any, Dict, List

import pytest

from src.utils import load_transactions


@pytest.fixture
def temp_json_file(tmp_path: Path) -> Any:
    """Фикстура для создания временного JSON-файла."""

    def _create_file(data: Any, filename: str = "operations.json") -> str:
        file_path = tmp_path / filename
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f)
        return str(file_path)

    return _create_file


def test_load_transactions_success(temp_json_file: Any) -> None:
    """Тест: успешная загрузка списка транзакций."""
    test_data: List[Dict[str, Any]] = [
        {"id": 1, "operationAmount": {"amount": "100", "currency": {"code": "USD"}}},
        {"id": 2, "operationAmount": {"amount": "200", "currency": {"code": "EUR"}}},
    ]
    file_path = temp_json_file(test_data)

    result = load_transactions(file_path)

    assert result == test_data
    assert len(result) == 2


def test_load_transactions_empty_list(temp_json_file: Any) -> None:
    """Тест: пустой список в файле."""
    file_path = temp_json_file([])
    result = load_transactions(file_path)
    assert result == []


def test_load_transactions_not_list(temp_json_file: Any) -> None:
    """Тест: файл содержит не список (например, словарь)."""
    file_path = temp_json_file({"key": "value"})
    result = load_transactions(file_path)
    assert result == []


def test_load_transactions_file_not_found() -> None:
    """Тест: файл не найден."""
    result = load_transactions("non_existent_file.json")
    assert result == []


def test_load_transactions_invalid_json(tmp_path: Path) -> None:
    """Тест: повреждённый JSON."""
    file_path = tmp_path / "invalid.json"
    with open(file_path, "w", encoding="utf-8") as f:
        f.write("{ invalid json }")

    result = load_transactions(str(file_path))
    assert result == []


def test_load_transactions_empty_file(tmp_path: Path) -> None:
    """Тест: пустой файл."""
    file_path = tmp_path / "empty.json"
    with open(file_path, "w", encoding="utf-8") as f:
        f.write("")

    result = load_transactions(str(file_path))
    assert result == []
