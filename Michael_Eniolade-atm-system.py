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
    # Create eight accounts and an ATM
    a1 = BankAccount("333333", "1234", balance=500.0)
    a2 = BankAccount("222222", "4321", balance=1200.0)
    a3 = BankAccount("111111", "5678", balance=800.0)
    a4 = BankAccount("444444", "9999", balance=1500.0)
    a5 = BankAccount("555555", "0000", balance=2000.0)
    a6 = BankAccount("666666", "7777", balance=3500.0)
    a7 = BankAccount("777777", "3333", balance=5000.0)
    a8 = BankAccount("888888", "2222", balance=10000.0)
    atm = ATM({"333333": a1, "222222": a2, "111111": a3, "444444": a4, "555555": a5, "666666": a6, "777777": a7, "888888": a8})

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

    # Test case with account 555555
    card5 = Card("555555", "0000")
    assert atm.insert_card(card5)
    assert atm.enter_pin("0000")

    print("\n--- Test Case 5 ---")
    print("Balance (a5):", atm.check_balance())                # 2000.0
    print("Withdraw:", atm.withdraw(500))                      # -> Withdrawal
    print("Balance (a5):", atm.check_balance())                # 1500.0
    print("Transfer to a3:", atm.transfer("111111", 300))      # -> Transfer
    print("Balance (a5):", atm.check_balance())                # 1200.0
    print("Balance (a3):", a3.balance)                         # 1100.0

    atm.eject()

    # Test case with account 666666
    card6 = Card("666666", "7777")
    assert atm.insert_card(card6)
    assert atm.enter_pin("7777")

    print("\n--- Test Case 6 ---")
    print("Balance (a6):", atm.check_balance())                # 3500.0
    print("Deposit:", atm.deposit(250))                        # -> Deposit
    print("Balance (a6):", atm.check_balance())                # 3750.0
    print("Withdraw:", atm.withdraw(1000))                     # -> Withdrawal
    print("Balance (a6):", atm.check_balance())                # 2750.0
    print("Transfer to a4:", atm.transfer("444444", 750))      # -> Transfer
    print("Balance (a6):", atm.check_balance())                # 2000.0
    print("Balance (a4):", a4.balance)                         # 2250.0

    atm.eject()

    # Test case with account 777777
    card7 = Card("777777", "3333")
    assert atm.insert_card(card7)
    assert atm.enter_pin("3333")

    print("\n--- Test Case 7 ---")
    print("Balance (a7):", atm.check_balance())                # 5000.0
    print("Deposit:", atm.deposit(500))                        # -> Deposit
    print("Balance (a7):", atm.check_balance())                # 5500.0
    print("Withdraw:", atm.withdraw(2000))                     # -> Withdrawal
    print("Balance (a7):", atm.check_balance())                # 3500.0
    print("Transfer to a2:", atm.transfer("222222", 1000))     # -> Transfer
    print("Balance (a7):", atm.check_balance())                # 2500.0
    print("Balance (a2):", a2.balance)                         # 2350.0
    print("Deposit again:", atm.deposit(100))                  # -> Deposit
    print("Balance (a7):", atm.check_balance())                # 2600.0

    atm.eject()

    # Test case with account 888888
    card8 = Card("888888", "2222")
    assert atm.insert_card(card8)
    assert atm.enter_pin("2222")

    print("\n--- Test Case 8 ---")
    print("Balance (a8):", atm.check_balance())                # 10000.0
    print("Withdraw:", atm.withdraw(3000))                     # -> Withdrawal
    print("Balance (a8):", atm.check_balance())                # 7000.0
    print("Transfer to a1:", atm.transfer("333333", 2000))     # -> Transfer
    print("Balance (a8):", atm.check_balance())                # 5000.0
    print("Balance (a1):", a1.balance)                         # 2400.0
    print("Withdraw again:", atm.withdraw(1500))               # -> Withdrawal
    print("Balance (a8):", atm.check_balance())                # 3500.0
    print("Deposit:", atm.deposit(500))                        # -> Deposit
    print("Balance (a8):", atm.check_balance())                # 4000.0

    atm.eject()

    # Test case with account 222222
    card2 = Card("222222", "4321")
    assert atm.insert_card(card2)
    assert atm.enter_pin("4321")

    print("\n--- Test Case 9 ---")
    print("Balance (a2):", atm.check_balance())                # 2350.0 (from previous transfers)
    print("Deposit:", atm.deposit(650))                        # -> Deposit
    print("Balance (a2):", atm.check_balance())                # 3000.0
    print("Transfer to a7:", atm.transfer("777777", 500))      # -> Transfer
    print("Balance (a2):", atm.check_balance())                # 2500.0
    print("Balance (a7):", a7.balance)                         # 3100.0
    print("Withdraw:", atm.withdraw(200))                      # -> Withdrawal
    print("Balance (a2):", atm.check_balance())                # 2300.0

    atm.eject()

    # Test case with account 111111
    card3 = Card("111111", "5678")
    assert atm.insert_card(card3)
    assert atm.enter_pin("5678")

    print("\n--- Test Case 10 ---")
    print("Balance (a3):", atm.check_balance())                # 1100.0 (from previous transfers)
    print("Withdraw:", atm.withdraw(300))                      # -> Withdrawal
    print("Balance (a3):", atm.check_balance())                # 800.0
    print("Deposit:", atm.deposit(1200))                       # -> Deposit
    print("Balance (a3):", atm.check_balance())                # 2000.0
    print("Transfer to a8:", atm.transfer("888888", 750))      # -> Transfer
    print("Balance (a3):", atm.check_balance())                # 1250.0
    print("Balance (a8):", a8.balance)                         # 4750.0
    print("Deposit again:", atm.deposit(250))                  # -> Deposit
    print("Balance (a3):", atm.check_balance())                # 1500.0

    atm.eject()

    # Test case with account 444444
    card4 = Card("444444", "9999")
    assert atm.insert_card(card4)
    assert atm.enter_pin("9999")

    print("\n--- Test Case 11 ---")
    print("Balance (a4):", atm.check_balance())                # 2250.0 (from previous transfers)
    print("Deposit:", atm.deposit(1750))                       # -> Deposit
    print("Balance (a4):", atm.check_balance())                # 4000.0
    print("Withdraw:", atm.withdraw(1000))                     # -> Withdrawal
    print("Balance (a4):", atm.check_balance())                # 3000.0
    print("Transfer to a6:", atm.transfer("666666", 500))      # -> Transfer
    print("Balance (a4):", atm.check_balance())                # 2500.0
    print("Balance (a6):", a6.balance)                         # 2500.0
    print("Withdraw again:", atm.withdraw(250))                # -> Withdrawal
    print("Balance (a4):", atm.check_balance())                # 2250.0

    atm.eject()
