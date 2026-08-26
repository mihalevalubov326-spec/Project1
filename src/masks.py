"""Модуль для маскировки номеров карт и счетов."""

from typing import Union

from src.logger_config import get_logger

logger = get_logger("masks")


def get_mask_card_number(number: Union[str, int]) -> str:
    """
    Маскирует номер банковской карты.

    Аргументы:
        number (Union[str, int]): Номер карты.

    Возвращает:
        str: Замаскированный номер карты.
    """
    logger.debug(f"Начало маскировки карты: {str(number)[:4]}...{str(number)[-4:]}")

    try:
        conv_number = str(number)

        if not conv_number:
            logger.error("Пустой номер карты")
            raise ValueError("Номер карты не может быть пустым")

        if len(conv_number) != 16:
            logger.warning(f"Нестандартная длина номера карты: {len(conv_number)} цифр")

        result = f"{conv_number[:4]} {conv_number[4:6]}** **** {conv_number[-4:]}"
        logger.info(f"Маскировка карты выполнена: {result}")
        return result

    except Exception as e:
        logger.error(f"Ошибка при маскировке карты: {e}", exc_info=True)
        raise


def get_mask_card_account(number: Union[str, int]) -> str:
    """
    Маскирует номер банковского счёта.

    Аргументы:
        number (Union[str, int]): Номер счёта.

    Возвращает:
        str: Замаскированный номер счёта.
    """
    logger.debug(f"Начало маскировки счёта: {str(number)[-4:]}...")

    try:
        conv_number = str(number)

        if not conv_number:
            logger.error("Пустой номер счёта")
            raise ValueError("Номер счёта не может быть пустым")

        result = f"**{conv_number[-4:]}"
        logger.info(f"Маскировка счёта выполнена: {result}")
        return result

    except Exception as e:
        logger.error(f"Ошибка при маскировке счёта: {e}", exc_info=True)
        raise
