from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Optional


# ---------------- Transaction ----------------
@dataclass
class Transaction:
    amount: float
    transaction_type: str
    timestamp: datetime = datetime.now()
    note: str = ""

    def __str__(self):
        amt = f"${self.amount:,.2f}"
        return f"[{self.timestamp:%Y-%m-%d %H:%M:%S}] {self.transaction_type}: {amt} {self.note}".strip()


# ---------------- BankAccount ----------------
class BankAccount:
    def __init__(self, account_number: str, pin: str, balance: float = 0.0, owner: str = "Customer"):
        self.account_number = account_number
        self.pin = pin
        self.balance = float(balance)
        self.owner = owner
        self.history: list[Transaction] = []

    # withdraw feature
    def withdraw(self, amount: float) -> Transaction:
        if amount <= 0:
            t = Transaction(0, "Error", note="Withdrawal amount must be positive")
            self.history.append(t)
            return t
        if amount <= self.balance:
            self.balance -= amount
            t = Transaction(amount, "Withdrawal")
            self.history.append(t)
            return t
        else:
            t = Transaction(0, "Error", note="Insufficient funds")
            self.history.append(t)
            return t

    # deposit feature
    def deposit(self, amount: float) -> Transaction:
        if amount <= 0:
            t = Transaction(0, "Error", note="Deposit amount must be positive")
            self.history.append(t)
            return t
        self.balance += amount
        t = Transaction(amount, "Deposit")
        self.history.append(t)
        return t

    # check balance feature
    def check_balance(self) -> float:
        self.history.append(Transaction(0, "Balance Inquiry"))
        return self.balance

    # money transfer feature from bank account
    def transfer(self, amount: float, bank_account: "BankAccount") -> Transaction:
        if amount <= 0:
            t = Transaction(0, "Error", note="Transfer amount must be positive")
            self.history.append(t)
            return t
        if amount <= self.balance:
            self.balance -= amount
            bank_account.balance += amount
            # record on sender
            t_out = Transaction(amount, "Transfer Out", note=f"to {bank_account.account_number}")
            self.history.append(t_out)
            # record on receiver
            bank_account.history.append(Transaction(amount, "Transfer In", note=f"from {self.account_number}"))
            return t_out
        else:
            t = Transaction(0, "Error", note="Insufficient funds")
            self.history.append(t)
            return t


# ---------------- Card ----------------
class Card:
    def __init__(self, card_number: str, pin: str, holder_name: str = "Customer"):
        self.card_number = card_number
        self.pin = pin
        self.holder_name = holder_name


# ---------------- ATM ----------------
class ATM:
    """
    Simple ATM that:
      - accepts a Card
      - authenticates with PIN (3 tries)
      - operates on the linked BankAccount
      - maintains cash_on_hand (optional realism)
    """
    def __init__(self, cash_on_hand: float = 2000.0):
        self.cash_on_hand = float(cash_on_hand)
        self.accounts: Dict[str, BankAccount] = {}  # account_number -> BankAccount
        self._inserted_card: Optional[Card] = None
        self._active_account: Optional[BankAccount] = None
        self._authed = False
        self._pin_attempts_left = 3

    def add_account(self, account: BankAccount):
        self.accounts[account.account_number] = account

    # --- session lifecycle ---
    def insert_card(self, card: Card):
        if self._inserted_card:
            raise ValueError("A card is already inserted.")
        # Validate card number exists in our registry
        if card.card_number not in self.accounts:
            raise ValueError("Unknown card/account.")
        self._inserted_card = card
        self._active_account = None
        self._authed = False
        self._pin_attempts_left = 3

    def enter_pin(self, pin: str) -> bool:
        if not self._inserted_card:
            raise ValueError("Insert a card first.")

        acct = self.accounts[self._inserted_card.card_number]
        if pin == acct.pin:
            self._active_account = acct
            self._authed = True
            self._pin_attempts_left = 3
            return True
        else:
            self._pin_attempts_left -= 1
            if self._pin_attempts_left <= 0:
                # simulate card capture
                self._capture_card()
                raise ValueError("Too many wrong PIN attempts. Card captured.")
            return False

    def _require_auth(self) -> BankAccount:
        if not self._authed or not self._active_account:
            raise ValueError("Not authenticated. Insert card and enter PIN.")
        return self._active_account

    def eject_card(self):
        if not self._inserted_card:
            raise ValueError("No card to eject.")
        self._inserted_card = None
        self._active_account = None
        self._authed = False
        self._pin_attempts_left = 3

    def _capture_card(self):
        # For simplicity, just clear state (card kept by ATM in real life)
        self._inserted_card = None
        self._active_account = None
        self._authed = False
        self._pin_attempts_left = 3

    # --- operations (delegate to BankAccount) ---
    def check_balance(self) -> float:
        acct = self._require_auth()
        return acct.check_balance()

    def deposit(self, amount: float) -> Transaction:
        if amount > 0:
            self.cash_on_hand += amount  # ATM receives cash
        acct = self._require_auth()
        return acct.deposit(amount)

    def withdraw(self, amount: float) -> Transaction:
        if amount > self.cash_on_hand:
            return Transaction(0, "Error", note="ATM does not have enough cash")
        acct = self._require_auth()
        tx = acct.withdraw(amount)
        if tx.transaction_type != "Error":
            self.cash_on_hand -= amount
        return tx

    def transfer(self, amount: float, to_account_number: str) -> Transaction:
        acct_from = self._require_auth()
        if to_account_number not in self.accounts:
            t = Transaction(0, "Error", note="Destination account not found")
            acct_from.history.append(t)
            return t
        acct_to = self.accounts[to_account_number]
        return acct_from.transfer(amount, acct_to)

    def recent_transactions(self, limit: int = 10) -> list[Transaction]:
        acct = self._require_auth()
        return acct.history[-limit:]


# --------------- Demo / CLI ---------------
def atm_system():
    atm = ATM(cash_on_hand=2500.0)

    # Demo accounts & cards
    alice = BankAccount(account_number="111111", pin="1234", balance=500.0, owner="Alice")
    bob   = BankAccount(account_number="222222", pin="4321", balance=1200.0, owner="Bob")
    charlie = BankAccount(account_number="333333", pin="5678", balance=800.0, owner="Charlie")
    atm.add_account(alice)
    atm.add_account(bob)
    atm.add_account(charlie)

    cards: Dict[str, Card] = {
        "1": Card(card_number="111111", pin="1234", holder_name="Alice"),
        "2": Card(card_number="222222", pin="4321", holder_name="Bob"),
        "3": Card(card_number="333333", pin="5678", holder_name="Charlie"),
    }

    print("Welcome to the ATM System!")
    print(f"(ATM cash on hand: ${atm.cash_on_hand:,.2f})")

    # Insert card
    while True:
        print("\nAvailable cards:")
        for k, c in cards.items():
            print(f"  {k}) {c.holder_name} (acct {c.card_number})")
        pick = input("Insert which card (1/2/3), or 'q' to quit: ").strip()
        if pick.lower() == "q":
            print("Goodbye.")
            return
        if pick in cards:
            try:
                atm.insert_card(cards[pick])
                print("Card inserted.")
                break
            except ValueError as e:
                print("ERROR:", e)
        else:
            print("Invalid selection.")

    # Authenticate
    while True:
        pin_try = input("Enter PIN: ").strip()
        try:
            ok = atm.enter_pin(pin_try)
            if ok:
                print("Access granted.")
                break
            else:
                print("Incorrect PIN. Try again.")
        except ValueError as e:
            print("ERROR:", e)
            return  # card captured / session ended

    # Menu loop
    while True:
        print("\nWhat would you like to do?")
        print("1. Withdraw")
        print("2. Deposit")
        print("3. Check Balance")
        print("4. Transfer")
        print("5. Recent Transactions")
        print("6. Eject Card / Exit")
        choice = input("Enter your choice (1-6): ").strip()

        try:
            if choice == "1":
                amount = float(input("Enter the amount to withdraw: "))
                tx = atm.withdraw(amount)
                print(tx)
                print(f"Your new balance is: ${atm.check_balance():,.2f}")
            elif choice == "2":
                amount = float(input("Enter the amount to deposit: "))
                tx = atm.deposit(amount)
                print(tx)
                print(f"Your new balance is: ${atm.check_balance():,.2f}")
            elif choice == "3":
                bal = atm.check_balance()
                print(f"Your current balance is: ${bal:,.2f}")
            elif choice == "4":
                to_acct = input("Enter the destination bank account number: ").strip()
                amount = float(input("Enter the amount to transfer: "))
                tx = atm.transfer(amount, to_acct)
                print(tx)
                print(f"Your new balance is: ${atm.check_balance():,.2f}")
            elif choice == "5":
                txs = atm.recent_transactions(10)
                if not txs:
                    print("No transactions yet.")
                else:
                    print("Recent transactions:")
                    for t in txs:
                        print("  ", t)
            elif choice == "6":
                atm.eject_card()
                print("Thank you for using the ATM System!")
                break
            else:
                print("Invalid option.")
        except ValueError as e:
            print("ERROR:", e)


if __name__ == "__main__":
    atm_system()
