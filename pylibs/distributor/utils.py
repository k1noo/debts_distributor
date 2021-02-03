import logging


def get_logger(object_name: str, level=logging.INFO):
    logger = logging.getLogger(object_name)
    logger.setLevel(level)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch = logging.StreamHandler()
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    return logger


def generate_user_id(name: str, index: int):
    return name.lower() + "_" + str(index)
