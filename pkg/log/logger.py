from loguru import logger
from datetime import datetime

INFO_LEVEL = "info"

def time_encoder(record):
    # Форматирование времени для записи
    return datetime.fromtimestamp(record["time"].timestamp()).strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]

def set_handler(level):
    # Настройка уровня логирования и формата
    logger.remove()  # Удаляем все предыдущие обработчики
    if level == INFO_LEVEL:
        logger.add(sys.stderr, format="{time} {level} {message}", level=level, serialize=False)
    else:
        logger.add(sys.stderr, format="{time} {level} {message}", level=level, serialize=False)

def verbosity(level: str):
    # Установка уровня логирования
    if level == "error":
        set_handler("ERROR")
    elif level == "info":
        set_handler("INFO")
    elif level == "debug":
        set_handler("DEBUG")
    else:
        set_handler("DEBUG")

# Пример использования
if __name__ == "__main__":
    verbosity("info")  # Установка уровня логирования
    logger.info("Это информационное сообщение")
    logger.debug("Это отладочное сообщение")
    logger.error("Это сообщение об ошибке")
