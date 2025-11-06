"""
Test suite for ATM System
"""
import pytest
from atm_system import BankAccount, Card, ATM, Transaction


class TestBankAccount:
    """Test cases for BankAccount class"""

    def test_deposit_increases_balance(self):
        """Test that depositing money increases the account balance correctly"""
        # Arrange
        account = BankAccount(account_number="123456", pin="1234", balance=1000.0, owner="Test User")
        initial_balance = account.balance
        deposit_amount = 500.0

        # Act
        account.deposit(deposit_amount)

        # Assert
        assert account.balance == initial_balance + deposit_amount
        assert account.balance == 1500.0
        assert len(account.history) == 1
        assert account.history[0].amount == deposit_amount
        assert account.history[0].transaction_type == "Deposit"