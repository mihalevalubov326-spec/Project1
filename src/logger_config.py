import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path


def setup_logger(
    module_name: str,
    log_dir: str = "logs",
    log_level: str = "INFO",
    console_output: bool = True,
    max_file_size: int = 5 * 1024 * 1024,  # 5 MB
    backup_count: int = 3,
) -> logging.Logger:
    """
    Настраивает и возвращает логгер для указанного модуля.

    Аргументы:
        module_name (str): Имя модуля (для имени файла лога).
        log_dir (str): Директория для хранения логов.
        log_level (str): Уровень логирования (DEBUG, INFO, WARNING, ERROR, CRITICAL).
        console_output (bool): Выводить ли логи в консоль.
        max_file_size (int): Максимальный размер файла лога в байтах.
        backup_count (int): Количество файлов логов для ротации.

    Возвращает:
        logging.Logger: Настроенный логгер.
    """
    # Создаём папку для логов, если её нет
    log_path = Path(log_dir)
    log_path.mkdir(parents=True, exist_ok=True)

    # Имя файла лога
    log_file = log_path / f"{module_name}.log"

    # Создаём логгер
    logger = logging.getLogger(module_name)
    logger.setLevel(getattr(logging, log_level.upper(), logging.INFO))

    # Очищаем существующие обработчики (чтобы не дублировать при повторных вызовах)
    if logger.handlers:
        logger.handlers.clear()

    # Формат логов: [ВРЕМЯ] [МОДУЛЬ] [УРОВЕНЬ] СООБЩЕНИЕ
    formatter = logging.Formatter(
        fmt="[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
    )

    # Обработчик для записи в файл (с ротацией)
    file_handler = RotatingFileHandler(log_file, maxBytes=max_file_size, backupCount=backup_count, encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # Обработчик для вывода в консоль (если включено)
    if console_output:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    return logger


def get_logger(module_name: str) -> logging.Logger:
    """
    Возвращает логгер для указанного модуля.
    Если логгер не был создан, создаёт его с настройками по умолчанию.

    Аргументы:
        module_name (str): Имя модуля.

    Возвращает:
        logging.Logger: Логгер модуля.
    """
    return setup_logger(module_name)
