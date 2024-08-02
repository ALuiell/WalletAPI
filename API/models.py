import uuid
from django.db import models
from django.contrib.auth.models import User
from .utils import generate_account_number


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class BankAccount(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bank_accounts')
    name = models.CharField(max_length=255, null=True, blank=True)
    account_number = models.CharField(max_length=8, unique=True, default=generate_account_number)
    balance = models.DecimalField(max_digits=15, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.user.username} - ({self.account_number})"


class Transaction(models.Model):
    bank_account = models.ForeignKey(BankAccount, on_delete=models.CASCADE, related_name='transactions')
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=255, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)

    TRANSACTION_TYPES = (
        ('income', 'Дохід'),
        ('expense', 'Витрата'),
        ('transfer', 'Переказ'),
    )
    type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)

    def __str__(self):
        return f"{self.bank_account} - {self.amount} ({self.type})"
