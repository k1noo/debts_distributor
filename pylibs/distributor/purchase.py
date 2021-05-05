from typing import List

from .transaction import Transaction
from .user import User
from .utils import get_logger
from .wallet import Wallet

logger = get_logger('Purchase')


class Purchase:

    def __init__(self, detached_wallet: Wallet, cost: float,
                 owners: List[User], description: str = None, timestamp: int = None):
        if not owners:
            raise RuntimeError('Attempt to create purchase without owners')

        self.__owners = owners
        self.__total_cost = cost
        self.__transactions = []

        cost_per_owner = cost // len(self.__owners)
        for owner in self.__owners:
            self.__transactions.append(Transaction(cost_per_owner, detached_wallet, owner.get_wallet(), timestamp))

        if description is not None:
            self.__description = description
        else:
            self.__description = 'Untitled purchase'

    def get_cost(self):
        return self.__total_cost

    def get_owners(self):
        for owner in self.__owners:
            yield owner

    def get_transactions(self):
        for transaction in self.__transactions:
            yield transaction

    def __str__(self):
        owners = [str(owner) for owner in self.get_owners()]
        return f'Purchase of cost: {self.get_cost()} for users: {", ".join(owners)}'
