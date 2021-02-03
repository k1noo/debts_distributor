from .wallet import Wallet


class Transaction:

    def __init__(self, amount: int, source: Wallet, destination: Wallet):
        self.__amount = amount
        self.___source = source
        self.__destination = destination

    def get_amount(self) -> int:
        return self.__amount

    def get_source(self) -> Wallet:
        return self.___source

    def get_destination(self) -> Wallet:
        return self.__destination
