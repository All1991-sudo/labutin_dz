import logging
import os


def setup_logger(name, log_file, level=logging.INFO):
    """Функция для настройки логирования"""
    module_dir = os.path.dirname(os.path.abspath(__file__))
    log_dir = os.path.join(module_dir, 'logs')

    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    log_file_path = os.path.join(log_dir, log_file)

    log_format = '%(asctime)s - %(name)s - %(levelname)s: %(message)s'
    logging.basicConfig(
        level=level,
        format=log_format,
        handlers=[
            logging.FileHandler(log_file_path, mode='w', encoding='utf-8'),
        ]
    )
    logger = logging.getLogger(name)
    return logger
