import datetime

from .constants import LOCAL_TZ
from .wallet import Wallet
from .utils import get_logger


logger = get_logger('Transaction')


class Transaction:

    def __init__(self, amount: float, source: Wallet, destination: Wallet, timestamp: float = None):
        self.__amount = amount
        self.__source = source
        self.__destination = destination
        if timestamp is not None:
            self.__timestamp = datetime.datetime.fromtimestamp(timestamp, tz=LOCAL_TZ)
        else:
            self.__timestamp = datetime.datetime.now(tz=LOCAL_TZ)
        self.__id = self.__generate_id()
        logger.info(f'Initiated {self}')

    def __generate_id(self) -> str:
        return f'{self.get_timestamp()}_{self.get_source().get_id()}_{self.get_destination().get_id()}'

    def get_amount(self) -> float:
        return self.__amount

    def get_source(self) -> Wallet:
        return self.__source

    def get_destination(self) -> Wallet:
        return self.__destination

    def get_timestamp(self) -> float:
        return self.__timestamp.timestamp()

    def get_id(self) -> str:
        return self.__id

    def __str__(self):
        return f'Transaction [{self.get_id()}]'

    def __hash__(self):
        return self.get_id()

    def __lt__(self, other):
        if self.get_timestamp() == other.get_timestamp():
            if self.get_source() == other.get_source():
                return self.get_destination() < other.get_destination()
            else:
                return self.get_source() < other.get_source()
        else:
            return self.get_timestamp() < other.get_timestamp()
