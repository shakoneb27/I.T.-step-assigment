class BankAccount:
   
    bank_name = "BOG"
    total_accounts = 0

    def __init__(self, card_type, owner, balance=0):
        self.card_type = card_type
        self.owner = owner
        self.__balance = 0          # private attribute
        self.balance = balance      # goes through the validating setter
        BankAccount.total_accounts += 1

    @property
    def balance(self):
        return self.__balance

    @balance.setter
    def balance(self, value):
        if value < self._min_balance():
            raise ValueError(
                f"Balance cannot be lower than {self._min_balance()} {self.currency_label()}."
            )
        self.__balance = value

    @balance.deleter
    def balance(self):
        print(f"Balance of {self.owner} has been reset to 0.")
        self.__balance = 0

    def _min_balance(self):
        """Lowest balance allowed for this account type."""
        return 0

    @staticmethod
    def currency_label():
        return "GEL"

    def deposit(self, amount):
        if amount <= 0:
            print("Deposit amount must be positive.")
            return False
        self.balance += amount
        print(f"{self.owner}: deposited {amount} GEL. Balance: {self.balance:.2f} GEL")
        return True

    def withdraw(self, amount):
        if amount <= 0:
            print("Withdrawal amount must be positive.")
            return False
        if amount > self.balance:
            print(f"{self.owner}: insufficient funds. Balance: {self.balance:.2f} GEL")
            return False
        self.balance -= amount
        print(f"{self.owner}: withdrew {amount} GEL. Balance: {self.balance:.2f} GEL")
        return True

    def __str__(self):
        return (
            f"[{self.bank_name}] {type(self).__name__} | {self.card_type} | "
            f"{self.owner} | Balance: {self.balance:.2f} GEL"
        )

    @classmethod
    def get_bank_info(cls):
        return f"Bank: {BankAccount.bank_name}, accounts created: {BankAccount.total_accounts}"

    @classmethod
    def set_bank_name(cls, new_name):
        BankAccount.bank_name = new_name
        print(f"Bank name changed to {BankAccount.bank_name}")

    @staticmethod
    def calculate_tax(amount, rate=1):
        """Tax (in percent) on an amount, independent of account type."""
        return amount * rate / 100


class SavingsAccount(BankAccount):
    def __init__(self, card_type, owner, balance=0, interest_rate=5, withdrawal_fee=1):
        super().__init__(card_type, owner, balance)
        self.interest_rate = interest_rate      # percent
        self.withdrawal_fee = withdrawal_fee    # percent of the withdrawn amount

    def apply_interest(self):
        interest = self.balance * self.interest_rate / 100
        self.balance += interest
        print(
            f"{self.owner}: interest {interest:.2f} GEL added "
            f"({self.interest_rate}%). Balance: {self.balance:.2f} GEL"
        )

    def withdraw(self, amount):
        if amount <= 0:
            print("Withdrawal amount must be positive.")
            return False
        fee = amount * self.withdrawal_fee / 100
        total = amount + fee
        if total > self.balance:
            print(
                f"{self.owner}: insufficient funds for {amount} GEL + {fee:.2f} GEL fee. "
                f"Balance: {self.balance:.2f} GEL"
            )
            return False
        self.balance -= total
        print(
            f"{self.owner}: withdrew {amount} GEL (fee {fee:.2f} GEL). "
            f"Balance: {self.balance:.2f} GEL"
        )
        return True


class CreditAccount(BankAccount):
    def __init__(self, card_type, owner, balance=0, credit_limit=2000):
        self.credit_limit = credit_limit   # set before super() because the setter uses it
        super().__init__(card_type, owner, balance)

    def _min_balance(self):
        return -self.credit_limit

    def withdraw(self, amount):
        if amount <= 0:
            print("Withdrawal amount must be positive.")
            return False
        if self.balance - amount < -self.credit_limit:
            available = self.balance + self.credit_limit
            print(
                f"{self.owner}: credit limit exceeded. "
                f"Available: {available:.2f} GEL"
            )
            return False
        self.balance -= amount
        print(f"{self.owner}: withdrew {amount} GEL. Balance: {self.balance:.2f} GEL")
        return True


if __name__ == "__main__":
    basic = BankAccount("Debit", "Giorgi", 500)
    savings = SavingsAccount("Savings", "Nino", 1000, interest_rate=5, withdrawal_fee=1)
    credit = CreditAccount("Credit", "Levan", 0, credit_limit=2000)

    print("--- Basic account ---")
    print(basic)
    basic.deposit(200)
    basic.withdraw(100)
    basic.withdraw(5000)     

    try:
        basic.balance = -50 
    except ValueError as e:
        print("Error:", e)

    print("--- Savings account ---")
    savings.apply_interest()
    savings.withdraw(200)    
    savings.withdraw(5000)

    print("--- Credit account ---")
    credit.withdraw(1500)    
    credit.withdraw(800)     
    credit.deposit(500)
    print(credit)

    print("--- Deleter ---")
    del basic.balance
    print(basic)

    print("--- Class and static methods ---")
    print(BankAccount.get_bank_info())
    BankAccount.set_bank_name("TBC")
    print(SavingsAccount.get_bank_info())
    print(f"Tax on 1000 GEL (1%): {BankAccount.calculate_tax(1000)} GEL")
    print(f"Tax on 1000 GEL (18%): {credit.calculate_tax(1000, 18)} GEL")