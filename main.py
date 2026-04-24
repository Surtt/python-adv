class BankAccount:
    accounts = []

    def __init__(
        self, account_holder: str, account_number: str | int, balance: int = 0
    ):
        self.account_holder = account_holder
        self.account_number = account_number
        self.balance = balance
        BankAccount.accounts.append(self)

    def deposit(self, amount: int):
        self.balance += amount

    def withdraw(self, amount: int):
        if self.balance < amount:
            print("Insufficient balance")
            return
        else:
            self.balance -= amount

    def transfer_to(self, other_account, amount):
        if self.balance < amount:
            print("Insufficient balance")
            return
        else:
            self.withdraw(amount)
            other_account.deposit(amount)

    def info(self):
        print(f"Balance: {self.balance}")

    @classmethod
    def get_accounts_created(cls):
        return len(cls.accounts)


account1 = BankAccount("John Doe", "123456789", 1000)
account2 = BankAccount("Jane Doe", "987654321")
print(account2.balance)

account2.deposit(500)
print(account2.balance)
account2.withdraw(200)
print(account2.balance)
account2.withdraw(1000)
print(account2.balance)
account1.transfer_to(account2, 200)
print(
    f"Account 1 balance: {account1.balance}", f"Account 2 balance: {account2.balance}"
)
account1.transfer_to(account2, 1000)
print(
    f"Account 1 balance: {account1.balance}", f"Account 2 balance: {account2.balance}"
)
account2.info()
print(BankAccount.get_accounts_created())
