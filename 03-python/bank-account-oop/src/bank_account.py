"""Bank account project: Encapsulation and Polymorphism (Python 3.9+)."""

from abc import ABC, abstractmethod
from datetime import datetime
from decimal import Decimal, InvalidOperation
from zoneinfo import ZoneInfo
import sys


DAYS_AR = (
    "الاثنين", "الثلاثاء", "الأربعاء", "الخميس",
    "الجمعة", "السبت", "الأحد",
)
MONTHS_AR = (
    "", "يناير", "فبراير", "مارس", "أبريل", "مايو", "يونيو",
    "يوليو", "أغسطس", "سبتمبر", "أكتوبر", "نوفمبر", "ديسمبر",
)
CURRENCY = "ريال"


def format_amount(value):
    """Format a monetary value without unnecessary trailing zeros."""
    return f"{value:,.2f}".rstrip("0").rstrip(".")


def parse_amount(value):
    """Accept positive SAR amounts with at most two decimal places."""
    try:
        if isinstance(value, bool):
            raise ValueError
        amount = Decimal(str(value))
        if (not amount.is_finite() or amount <= 0 or
                amount != amount.quantize(Decimal("0.01"))):
            raise ValueError
        return amount
    except (InvalidOperation, ValueError):
        raise ValueError("المبلغ غير صحيح. أدخل رقمًا موجبًا حتى منزلتين عشريتين.")


def arabic_timestamp(moment):
    """Day, date and 12-hour time in Arabic, e.g. 4:45am."""
    hour = moment.hour % 12 or 12
    period = "am" if moment.hour < 12 else "pm"
    return (
        f"يوم {DAYS_AR[moment.weekday()]}، {moment.day} "
        f"{MONTHS_AR[moment.month]} {moment.year}، "
        f"الساعة {hour}:{moment.minute:02d}{period}"
    )


class BankAccount:
    """A bank account with an encapsulated, read-only balance."""

    def __init__(self, owner):
        self.owner = owner
        self.__balance = Decimal("0.00")  # Encapsulation

    @property
    def balance(self):
        """Read the current balance without changing it directly."""
        return self.__balance

    def deposit(self, amount, when=None):
        amount = parse_amount(amount)
        self.__balance += amount
        moment = when if when is not None else datetime.now(ZoneInfo("Asia/Riyadh"))
        print(
            f"تم إيداع {format_amount(amount)} {CURRENCY} لرصيدك البنكي "
            f"في {arabic_timestamp(moment)}."
        )
        return True

    def withdraw(self, amount, when=None):
        amount = parse_amount(amount)
        if amount > self.__balance:
            print("لا يمكن السحب: الرصيد غير كافٍ.")
            return False
        self.__balance -= amount
        moment = when if when is not None else datetime.now(ZoneInfo("Asia/Riyadh"))
        print(
            f"تم خصم {format_amount(amount)} {CURRENCY} من رصيدك البنكي "
            f"في {arabic_timestamp(moment)}."
        )
        return True

    def show_balance(self):
        print(f"الرصيد الحالي لـ {self.owner}: {format_amount(self.balance)} {CURRENCY}")
        return self.balance


class Transaction(ABC):
    """Parent class: each transaction implements the same method."""

    def __init__(self, amount):
        self.amount = amount

    @abstractmethod
    def process(self, account):
        pass


class DepositTransaction(Transaction):
    def process(self, account):  # Polymorphism
        return account.deposit(self.amount)


class WithdrawalTransaction(Transaction):
    def process(self, account):  # Polymorphism
        return account.withdraw(self.amount)


def demo():
    account = BankAccount("Ahmed")
    print("--- حساب بنكي جديد ---")
    account.show_balance()

    # One method call has different behavior for each transaction type.
    transactions = [DepositTransaction(2000), WithdrawalTransaction(150)]
    for transaction in transactions:
        transaction.process(account)

    account.show_balance()
    WithdrawalTransaction(5000).process(account)  # Insufficient funds
    account.show_balance()


def interactive_mode():
    name = input("اسم صاحب الحساب: ").strip() or "مستخدم"
    account = BankAccount(name)
    while True:
        print("\n1) إيداع  2) سحب  3) الاستعلام عن الرصيد  4) خروج")
        option = input("اختر العملية: ").strip()
        if option == "4":
            print("شكرًا لاستخدامك البرنامج.")
            break
        if option == "3":
            account.show_balance()
        elif option in ("1", "2"):
            amount = input("أدخل المبلغ بالريال: ").strip()
            transaction = (DepositTransaction(amount) if option == "1"
                           else WithdrawalTransaction(amount))
            try:
                transaction.process(account)
            except ValueError as error:
                print(error)
        else:
            print("خيار غير صحيح.")


if __name__ == "__main__":
    if "--interactive" in sys.argv:
        interactive_mode()
    else:
        demo()