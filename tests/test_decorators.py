import os
import sys
from typing import Any

import pytest

from src.decorators import log

# Добавляем корневую папку проекта в путь поиска модулей
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


def test_log_success(capsys: pytest.CaptureFixture) -> None:
    """Тест: успешное выполнение функции, логи в консоль."""

    @log
    def add(a: int, b: int) -> int:
        return a + b

    result = add(3, 5)
    captured = capsys.readouterr()

    assert result == 8
    assert "Вызов функции 'add'" in captured.out
    assert "Результат: 8" in captured.out


def test_log_error(capsys: pytest.CaptureFixture) -> None:
    """Тест: функция вызывает ошибку, логи в консоль."""

    @log
    def divide(a: int, b: int) -> float:
        return a / b

    with pytest.raises(ZeroDivisionError):
        divide(10, 0)

    captured = capsys.readouterr()
    assert "Вызов функции 'divide'" in captured.out
    assert "Ошибка в функции 'divide': ZeroDivisionError" in captured.out


def test_log_with_args(capsys: pytest.CaptureFixture) -> None:
    """Тест: функция с kwargs, логи в консоль."""

    @log
    def greet(name: str, greeting: str = "Привет") -> str:
        return f"{greeting}, {name}!"

    result = greet("Анна", greeting="Здравствуйте")
    captured = capsys.readouterr()

    assert result == "Здравствуйте, Анна!"
    assert "args=('Анна',)" in captured.out
    assert "kwargs={'greeting': 'Здравствуйте'}" in captured.out
    assert "Результат: Здравствуйте, Анна!" in captured.out


def test_log_no_args(capsys: pytest.CaptureFixture) -> None:
    """Тест: функция без аргументов."""

    @log
    def say_hello() -> str:
        return "Hello!"

    result = say_hello()
    captured = capsys.readouterr()

    assert result == "Hello!"
    assert "без аргументов" in captured.out


def test_log_multiple_calls(capsys: pytest.CaptureFixture) -> None:
    """Тест: несколько вызовов одной функции."""

    @log
    def multiply(a: int, b: int) -> int:
        return a * b

    multiply(2, 3)
    multiply(4, 5)
    captured = capsys.readouterr()

    assert captured.out.count("Вызов функции 'multiply'") == 2
    assert captured.out.count("Результат: 6") == 1
    assert captured.out.count("Результат: 20") == 1


def test_log_to_file_success(tmp_path: pytest.TempPathFactory) -> None:
    """Тест: успешное выполнение, логи в файл."""
    log_file = tmp_path / "log.txt"

    @log(filename=str(log_file))
    def add(a: int, b: int) -> int:
        return a + b

    result = add(3, 5)
    content = log_file.read_text(encoding="utf-8")

    assert result == 8
    assert "Вызов функции 'add'" in content
    assert "Результат: 8" in content


def test_log_to_file_error(tmp_path: pytest.TempPathFactory) -> None:
    """Тест: функция с ошибкой, логи в файл."""
    log_file = tmp_path / "error_log.txt"

    @log(filename=str(log_file))
    def divide(a: int, b: int) -> float:
        return a / b

    with pytest.raises(ZeroDivisionError):
        divide(10, 0)

    content = log_file.read_text(encoding="utf-8")
    assert "Вызов функции 'divide'" in content
    assert "Ошибка в функции 'divide': ZeroDivisionError" in content
    assert "Входные параметры: args=(10, 0)" in content


def test_log_to_file_append(tmp_path: pytest.TempPathFactory) -> None:
    """Тест: несколько вызовов, логи добавляются в файл (режим append)."""
    log_file = tmp_path / "append_log.txt"

    @log(filename=str(log_file))
    def add(a: int, b: int) -> int:
        return a + b

    add(1, 2)
    add(3, 4)

    content = log_file.read_text(encoding="utf-8")
    lines = content.strip().split("\n")

    assert len(lines) == 4  # 2 вызова × 2 строки (начало + результат)
    assert "Результат: 3" in content
    assert "Результат: 7" in content


def test_log_to_file_with_kwargs(tmp_path: pytest.TempPathFactory) -> None:
    """Тест: функция с именованными аргументами, логи в файл."""
    log_file = tmp_path / "kwargs_log.txt"

    @log(filename=str(log_file))
    def power(base: int, exponent: int = 2) -> int:
        return base**exponent

    result = power(5, exponent=3)
    content = log_file.read_text(encoding="utf-8")

    assert result == 125
    assert "kwargs={'exponent': 3}" in content


def test_log_without_parentheses(capsys: pytest.CaptureFixture) -> None:
    """Тест: использование декоратора без скобок @log."""

    @log
    def square(x: int) -> int:
        return x**2

    result = square(4)
    captured = capsys.readouterr()

    assert result == 16
    assert "Вызов функции 'square'" in captured.out
    assert "Результат: 16" in captured.out


def test_log_with_empty_parentheses(capsys: pytest.CaptureFixture) -> None:
    """Тест: использование декоратора с пустыми скобками @log()."""

    @log()
    def double(x: int) -> int:
        return x * 2

    result = double(5)
    captured = capsys.readouterr()

    assert result == 10
    assert "Вызов функции 'double'" in captured.out


def test_log_value_error(capsys: pytest.CaptureFixture) -> None:
    """Тест: перехват ValueError."""

    @log
    def parse_int(s: str) -> int:
        return int(s)

    with pytest.raises(ValueError):
        parse_int("not a number")

    captured = capsys.readouterr()
    assert "Ошибка в функции 'parse_int': ValueError" in captured.out


def test_log_type_error(capsys: pytest.CaptureFixture) -> None:
    """Тест: перехват TypeError."""

    @log
    def add(a: int, b: int) -> int:
        return a + b

    with pytest.raises(TypeError):
        add("1", 2)  # type: ignore

    captured = capsys.readouterr()
    assert "Ошибка в функции 'add': TypeError" in captured.out


def test_log_key_error(capsys: pytest.CaptureFixture) -> None:
    """Тест: перехват KeyError."""

    @log
    def get_value(data: dict, key: str) -> Any:
        return data[key]

    with pytest.raises(KeyError):
        get_value({}, "missing")

    captured = capsys.readouterr()
    assert "Ошибка в функции 'get_value': KeyError" in captured.out


def test_log_return_list(capsys: pytest.CaptureFixture) -> None:
    """Тест: функция возвращает список."""

    @log
    def get_list() -> list:
        return [1, 2, 3]

    result = get_list()
    captured = capsys.readouterr()

    assert result == [1, 2, 3]
    assert "Результат: [1, 2, 3]" in captured.out


def test_log_return_dict(capsys: pytest.CaptureFixture) -> None:
    """Тест: функция возвращает словарь."""

    @log
    def get_dict() -> dict:
        return {"a": 1, "b": 2}

    result = get_dict()
    captured = capsys.readouterr()

    assert result == {"a": 1, "b": 2}
    assert "Результат: {'a': 1, 'b': 2}" in captured.out


def test_log_return_none(capsys: pytest.CaptureFixture) -> None:
    """Тест: функция ничего не возвращает (None)."""

    @log
    def do_nothing() -> None:
        pass

    result = do_nothing()
    captured = capsys.readouterr()

    assert result is None
    assert "Результат: None" in captured.out
