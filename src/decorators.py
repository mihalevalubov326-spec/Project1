import datetime
import functools
from typing import Any, Callable, Optional


def log(filename: Optional[str] = None) -> Callable:
    """
    Декоратор для логирования начала, конца и результатов выполнения функции.

    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            # Получаем текущее время
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Формируем строку с именем функции и аргументами
            func_name = func.__name__
            args_str = f"args={args}, kwargs={kwargs}" if args or kwargs else "без аргументов"

            # Логируем начало выполнения
            start_msg = f"[{timestamp}] Вызов функции '{func_name}' с {args_str}"
            _log_message(start_msg, filename)

            try:
                # Выполняем функцию
                result = func(*args, **kwargs)

                # Логируем успешное завершение с результатом
                end_msg = f"[{timestamp}] Функция '{func_name}' завершила работу. Результат: {result}"
                _log_message(end_msg, filename)

                return result

            except Exception as e:
                # Логируем ошибку
                error_msg = f"[{timestamp}] Ошибка в функции '{func_name}': {type(e).__name__}: {e}. Входные параметры: {args_str}"
                _log_message(error_msg, filename)

                # Пробрасываем исключение дальше
                raise

        return wrapper

    if callable(filename):
        # Случай: @log (без скобок и без аргументов)
        func = filename
        filename = None
        return decorator(func)

    # Случай: @log() или @log(filename="log.txt")
    return decorator


def _log_message(message: str, filename: Optional[str]) -> None:
    """Вспомогательная функция для записи сообщения в файл или консоль."""
    if filename:
        with open(filename, "a", encoding="utf-8") as f:
            f.write(message + "\n")
    else:
        print(message)


@log
def add(a: int, b: int) -> int:
    return a + b


result = add(5, 3)
print(f"Результат: {result}")


@log(filename="log.txt")
def divide(a: int, b: int) -> float:
    return a / b


# Успешный вызов
result = divide(10, 2)
print(f"Результат: {result}")

# Вызов с ошибкой
try:
    divide(10, 0)
except ZeroDivisionError:
    print("Поймали ошибку деления на ноль")
