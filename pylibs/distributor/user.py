from .utils import generate_user_id
from .utils import get_logger


class User:

    def __init__(self, name: str, index: int):
        self.__name = name
        self.__id = generate_user_id(name, index)
        self.__logger = get_logger("User_" + self.__id)

    def get_name(self):
        return self.__name

    def get_id(self):
        return self.__id
