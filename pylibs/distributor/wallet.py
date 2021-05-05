from queue import PriorityQueue

from .transaction import Transaction
from .utils import get_logger, generate_random_id


logger = get_logger('Wallet')


class Wallet:

    def __init__(self):
        self.__id = f'w_{generate_random_id()}'
        self.__state = 0.0
        self.__incoming_transactions = PriorityQueue()
        self.__outgoing_transactions = PriorityQueue()

    def get_id(self) -> str:
        return self.__id

    def get_state(self) -> float:
        return self.__state

    def get_state_report(self) -> str:
        return f'State of {str(self)}: balance = {self.__state}, ' \
               f'income count = {self.__incoming_transactions.qsize()}, ' \
               f'outgoing count = {self.__outgoing_transactions.qsize()}'

    def account_transaction(self, transaction: Transaction):
        source_wallet = transaction.get_source()
        destination_wallet = transaction.get_destination()
        logger.info('Accounting ' + str(transaction) + ' to ' + str(self))
        if self.get_id() == source_wallet.get_id():
            self.__account_outgoing_transaction(transaction)
        elif self.get_id() == destination_wallet.get_id():
            self.__account_incoming_transaction(transaction)
        else:
            raise RuntimeError('Attempt to account ' + str(transaction) + ' to ' + str(self))
        logger.info(f'Updated{str(self)}. {self.get_state_report()}')

    def __account_incoming_transaction(self, transaction: Transaction):
        self.__state += transaction.get_amount()
        self.__incoming_transactions.put(transaction)

    def __account_outgoing_transaction(self, transaction: Transaction):
        self.__state -= transaction.get_amount()
        self.__outgoing_transactions.put(transaction)

    def __str__(self):
        return f'Wallet [{self.get_id()}]'

    def __hash__(self):
        return self.get_id()

    def __lt__(self, other):
        return self.get_id() < other.get_id()
