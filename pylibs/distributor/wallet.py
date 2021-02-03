from .transaction import Transaction


class Wallet:

    def __init__(self, wallet_id: str):
        self.__id = wallet_id
        self.__state = 0
        self.__income_transactions = list()
        self.__outgoing_transactions = list()

    def get_id(self):
        return self.__id

    def account_transaction(self, transaction: Transaction):
        source_wallet = transaction.get_source()
        destination_wallet = transaction.get_destination()
        if self.__id == source_wallet.get_id():
            self.__state -= transaction.get_amount()
            self.__outgoing_transactions.append(transaction)
        elif self.__id == destination_wallet.get_id():
            self.__state += transaction.get_amount()
            self.__income_transactions.append(transaction)
