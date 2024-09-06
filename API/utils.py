import random


def generate_account_number():
    from .models import BankAccount
    while True:
        digits = list(range(10))
        random.shuffle(digits)
        account_number = ''.join(map(str, digits[:8]))
        if not BankAccount.objects.filter(account_number=account_number).exists():
            return account_number

