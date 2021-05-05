import logging
import uuid


def get_logger(object_name: str, level=logging.INFO):
    logger = logging.getLogger(object_name)
    logger.setLevel(level)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch = logging.StreamHandler()
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    return logger


def generate_random_id():
    return str(uuid.uuid4())[-8:]


def is_zero(x: float):
    return abs(x) <= 1e-6
