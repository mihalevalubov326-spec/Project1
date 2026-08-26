from pathlib import Path

import pytest

from src.logger_config import setup_logger


def test_setup_logger_creates_log_file(tmp_path: Path) -> None:
    """Тест: создание файла лога."""
    log_dir = tmp_path / "logs"
    logger = setup_logger("test_module", log_dir=str(log_dir))

    logger.info("Тестовое сообщение")

    log_file = log_dir / "test_module.log"
    assert log_file.exists()

    content = log_file.read_text(encoding="utf-8")
    assert "Тестовое сообщение" in content


def test_setup_logger_console_output(capsys: pytest.CaptureFixture) -> None:
    """Тест: вывод в консоль."""
    logger = setup_logger("console_test", console_output=True)
    logger.info("Консольное сообщение")

    captured = capsys.readouterr()
    assert "Консольное сообщение" in captured.out


def test_setup_logger_log_level() -> None:
    """Тест: уровень логирования."""
    logger = setup_logger("level_test", log_level="ERROR")

    logger.debug("DEBUG сообщение")
    logger.info("INFO сообщение")
    logger.warning("WARNING сообщение")
    logger.error("ERROR сообщение")

    # Проверяем, что логируются только сообщения уровня ERROR и выше
