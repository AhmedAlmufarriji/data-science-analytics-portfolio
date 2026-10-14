# Bank Account Simulation (OOP)

A practice account system demonstrating encapsulation and polymorphic transaction processing.

**Stack:** Python standard library; Decimal and zoneinfo

## Features

- New accounts start with a zero balance.
- Positive, two-decimal-place deposits and withdrawals.
- Rejected overdrafts and invalid amounts.
- Timestamped Arabic receipts using the Asia/Riyadh time zone.
- `BankAccount`, `Transaction`, `DepositTransaction` and `WithdrawalTransaction`.

**Important:** This is not a banking application, financial ledger, secure account service or production-grade transaction processor.

## How to get started

```bash
python src/bank_account.py
```

See the Python tests under [tests](../../tests/test_portfolio.py).
