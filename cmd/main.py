import logging
from config import get_config  # Предположим, что у вас есть аналогичная функция в config.py
from server import NewServer  # Предположим, что у вас есть аналогичная функция в server.py

def main():
    # Получаем конфигурацию
    cfg = get_config()

    # Устанавливаем уровень логирования
    logging.basicConfig(level=cfg['log_level'])
    logger = logging.getLogger(__name__)

    # Создаем сервер
    try:
        srv = NewServer(cfg)
    except Exception as e:
        logger.fatal(f"Ошибка при создании сервера: {e}")
        return

    # Запускаем сервер
    try:
        srv.run()
    except Exception as e:
        logger.fatal(f"Ошибка при запуске сервера: {e}")

if __name__ == "__main__":
    main()
