import copy

from .purchase import Purchase
from .utils import generate_random_id, get_logger, is_zero
from .wallet import Wallet
from .user import User
from .transaction import Transaction


class Session:

    def __init__(self):
        self.__id = f's_{generate_random_id()}'
        self.__wallet = Wallet()
        self.__logger = get_logger(f'Session_{self.get_id()}')

        self.__users = dict()

    def get_id(self):
        return self.__id

    def register_user(self, name: str, user_id: str = None) -> str:
        new_user = User(name, user_id)
        self.__logger.info(f'Trying to register {new_user}')
        if new_user.get_id() not in self.__users.keys():
            self.__users[new_user.get_id()] = new_user
        else:
            raise RuntimeError(f'Attempt to register existing {new_user}')
        return new_user.get_id()

    def account_purchase(self, cost: float, user_ids: list, description: str = None):
        if not user_ids:
            return
        purchase_owners = []
        for user_id in user_ids:
            if user_id in self.__users.keys():
                purchase_owners.append(self.__users.get(user_id))
        purchase = Purchase(self.__wallet, cost, purchase_owners, description)
        self.__logger.info(f'Processing new purchase: {purchase}')
        for transaction in purchase.get_transactions():
            self.__process_transaction(transaction.get_source(),
                                       transaction.get_destination(),
                                       transaction.get_amount())

    def account_user_to_common_transaction(self, user_id: str, amount: float):
        user = self.__users.get(user_id, None)
        if user is None:
            return
        self.__process_transaction(user.get_wallet(), self.__wallet, amount)

    def account_common_to_user_transaction(self, user_id: str, amount: float):
        user = self.__users.get(user_id, None)
        if user is None:
            return
        self.__process_transaction(self.__wallet, user.get_wallet(), amount)

    def account_user_to_user_transaction(self, src_user_id: str, dst_user_id: str, amount: float):
        src_user = self.__users.get(src_user_id, None)
        dst_user = self.__users.get(dst_user_id, None)
        if src_user is None or dst_user is None:
            return
        self.__process_transaction(src_user.get_wallet(), dst_user.get_wallet(), amount)

    def distribute_debts(self):
        if not is_zero(self.__wallet.get_state()):
            self.__logger.info(f'Unable to distribute debts before bills are paid')
            return None
        current_users_state = copy.deepcopy(self.__users)
        compensation_transactions = []
        negative_balance_wallet, positive_balance_wallet = self.__get_opposite_wallets(current_users_state)
        while negative_balance_wallet is not None and positive_balance_wallet is not None:
            transaction = self.__generate_compensation_transaction(negative_balance_wallet, positive_balance_wallet)
            negative_balance_wallet.account_transaction(transaction)
            positive_balance_wallet.account_transaction(transaction)
            compensation_transactions.append(transaction)
            negative_balance_wallet, positive_balance_wallet = self.__get_opposite_wallets(current_users_state)
        compensation_transactions = sorted(compensation_transactions, key=lambda t: t.get_source())
        self.__logger.info(f'Generated compensation transactions: {compensation_transactions}')
        return compensation_transactions

    def __process_transaction(self, src: Wallet, dst: Wallet, amount: float):
        transaction = Transaction(amount, src, dst)
        self.__logger.info(f'Processing {transaction}')
        src.account_transaction(transaction)
        dst.account_transaction(transaction)
        self.__logger.info(f'New wallet state: {src}')
        self.__logger.info(f'New wallet state: {dst}')

    @staticmethod
    def __get_opposite_wallets(users):
        non_zero_wallet_users = [user for user in users if not is_zero(user.get_wallet().get_state())]
        if len(non_zero_wallet_users) < 2:
            return None, None
        non_zero_wallet_users = sorted(non_zero_wallet_users, key=lambda user: user.get_wallet().get_state())
        return non_zero_wallet_users[0], non_zero_wallet_users[-1]

    @staticmethod
    def __generate_compensation_transaction(negative_balance_wallet: Wallet, positive_balance_wallet: Wallet):
        available_amount = positive_balance_wallet.get_state()
        compensable = abs(negative_balance_wallet.get_state())
        amount_to_transact = min(available_amount, compensable)
        return Transaction(amount_to_transact, positive_balance_wallet, negative_balance_wallet)
