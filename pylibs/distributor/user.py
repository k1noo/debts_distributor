from .wallet import Wallet

from .utils import generate_random_id
from .utils import get_logger


class User:

    def __init__(self, name: str, user_id: str = None):
        self.__name = name
        if user_id is not None:
            self.__id = user_id
        else:
            self.__id = f'u_{name.lower()}_{generate_random_id()}'
        self.__logger = get_logger("User_" + self.__id)
        self.__wallet = Wallet()
        self.__logger.info(f'Created [{str(self)}]')

    def get_name(self) -> str:
        return self.__name

    def get_id(self) -> str:
        return self.__id

    def get_wallet(self) -> Wallet:
        return self.__wallet

    def __str__(self):
        return f'User [id:{self.get_id()}|name:{self.get_name()}]'
