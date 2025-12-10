
import unittest

class Test_bank_Prabu_accounts(unittest.TestCase):

    def __init__(self, name, balance=0):
        self.name = name
        self.balance = balance

    def deposit(self, amount):
        self.balance += amount
        print(f"{amount} deposited successfully.")

    def withdraw(self, amount):
        if amount > self.balance:
            print("Insufficient balance!")
        else:
            self.balance -= amount
            print(f"{amount} withdrawn successfully.")

    def check_balance(self):
        print(f"Account Holder: {self.name}")
        print(f"Available Balance: {self.balance}")




# acc1 = BankAccount("Prabu", 1000)


