class Transaction:
    def __init__(self, ttype: str, amount: float):
        self.type = ttype
        self.amount = amount

    def __repr__(self):
        return f"Transaction(type='{self.type}', amount={self.amount})"


class BankAccount:
    def __init__(self, account_number: str, pin: str, balance: float = 0.0):
        self.account_number = account_number
        self.pin = pin
        self.balance = float(balance)

    def deposit(self, amount: float) -> Transaction:
        if amount <= 0:
            return Transaction("Error", 0)
        self.balance += amount
        return Transaction("Deposit", amount)

    def withdraw(self, amount: float) -> Transaction:
        if amount <= 0 or amount > self.balance:
            return Transaction("Error", 0)
        self.balance -= amount
        return Transaction("Withdrawal", amount)

    def transfer(self, amount: float, other: "BankAccount") -> Transaction:
        if amount <= 0 or amount > self.balance or self.account_number == other.account_number:
            return Transaction("Error", 0)
        self.balance -= amount
        other.balance += amount
        return Transaction("Transfer", amount)


class Card:
    def __init__(self, account_number: str, pin: str):
        self.account_number = account_number
        self.pin = pin


class ATM:
    def __init__(self, accounts: dict[str, BankAccount]):
        self.accounts = accounts
        self._card: Card | None = None
        self._account: BankAccount | None = None

    def insert_card(self, card: Card) -> bool:
        if card.account_number in self.accounts:
            self._card = card
            return True
        return False

    def enter_pin(self, pin: str) -> bool:
        if not self._card:
            return False
        acct = self.accounts[self._card.account_number]
        if pin == acct.pin:
            self._account = acct
            return True
        return False

    def eject(self):
        self._card = None
        self._account = None

    # Operations
    def check_balance(self) -> float:
        return self._account.balance if self._account else 0.0

    def deposit(self, amount: float) -> Transaction:
        return self._account.deposit(amount) if self._account else Transaction("Error", 0)

    def withdraw(self, amount: float) -> Transaction:
        return self._account.withdraw(amount) if self._account else Transaction("Error", 0)

    def transfer(self, to_account_number: str, amount: float) -> Transaction:
        if not self._account or to_account_number not in self.accounts:
            return Transaction("Error", 0)
        return self._account.transfer(amount, self.accounts[to_account_number])


# runnign the demo
if __name__ == "__main__":
    # Create four accounts and an ATM
    a1 = BankAccount("333333", "1234", balance=500.0)
    a2 = BankAccount("222222", "4321", balance=1200.0)
    a3 = BankAccount("111111", "5678", balance=800.0)
    a4 = BankAccount("444444", "9999", balance=1500.0)
    atm = ATM({"333333": a1, "222222": a2, "111111": a3, "444444": a4})

    # Use a card for account 333333
    card = Card("333333", "1234")
    assert atm.insert_card(card)
    assert atm.enter_pin("1234")

    print("Balance:", atm.check_balance())                # 500.0
    print("Deposit:", atm.deposit(100))                   # -> Deposit
    print("Balance:", atm.check_balance())                # 600.0
    print("Withdraw:", atm.withdraw(50))                  # -> Withdrawal
    print("Balance:", atm.check_balance())                # 550.0
    print("Transfer:", atm.transfer("222222", 150))       # -> Transfer
    print("Balance (a1):", atm.check_balance())           # 400.0
    print("Balance (a2):", a2.balance)                    # 1350.0

    atm.eject()
