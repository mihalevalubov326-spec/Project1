"""Модуль для работы с транзакциями."""

import json
import os
from typing import Any, Dict, List, Optional

from src.logger_config import get_logger

logger = get_logger("utils")


def load_transactions(file_path: str) -> List[Dict[str, Any]]:
    """
    Загружает транзакции из JSON-файла.

    Аргументы:
        file_path (str): Путь к JSON-файлу.

    Возвращает:
        List[Dict[str, Any]]: Список транзакций. В случае ошибки — пустой список.
    """
    logger.info(f"Загрузка транзакций из файла: {file_path}")

    try:
        if not os.path.exists(file_path):
            logger.warning(f"Файл не найден: {file_path}")
            return []

        file_size = os.path.getsize(file_path)
        logger.debug(f"Размер файла: {file_size} байт")

        if file_size == 0:
            logger.warning(f"Файл пустой: {file_path}")
            return []

        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        logger.debug(f"Загружены данные: {type(data).__name__}")

        if isinstance(data, list):
            logger.info(f"Успешно загружено {len(data)} транзакций")
            return data

        logger.warning(f"Файл содержит не список, а {type(data).__name__}")
        return []

    except json.JSONDecodeError as e:
        logger.error(f"Ошибка парсинга JSON: {e}")
        return []

    except Exception as e:
        logger.error(f"Неизвестная ошибка при загрузке файла: {e}", exc_info=True)
        return []


def get_operation_amount(transaction: Dict[str, Any]) -> Optional[float]:
    """
    Извлекает сумму транзакции.

    Аргументы:
        transaction (Dict[str, Any]): Словарь транзакции.

    Возвращает:
        Optional[float]: Сумма транзакции или None при ошибке.
    """
    logger.debug(f"Извлечение суммы из транзакции: {transaction.get('id', 'unknown')}")

    try:
        operation_amount = transaction.get("operationAmount")

        if operation_amount is None:
            logger.warning("Поле operationAmount отсутствует")
            return None

        amount_str = operation_amount.get("amount")

        if amount_str is None:
            logger.warning("Поле amount отсутствует")
            return None

        amount = float(amount_str)
        logger.debug(f"Извлечена сумма: {amount}")
        return amount

    except (ValueError, TypeError) as e:
        logger.error(f"Ошибка при извлечении суммы: {e}")
        return None
