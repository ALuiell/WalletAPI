from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Transaction, BankAccount


@receiver(post_save, sender=Transaction)
def update_balance_on_transaction_save(sender, instance, created, **kwargs):
    if created or instance.type == 'transfer':
        instance.bank_account.balance += instance.amount if instance.type == 'income' else -instance.amount
        instance.bank_account.save()


@receiver(post_delete, sender=Transaction)
def update_balance_on_transaction_delete(sender, instance, **kwargs):
    instance.bank_account.balance -= instance.amount if instance.type == 'income' else -instance.amount
    instance.bank_account.save()
