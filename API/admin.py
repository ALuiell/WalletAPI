from django.contrib import admin
from .models import Category, Transaction, BankAccount

admin.site.register(BankAccount)
admin.site.register(Category)
admin.site.register(Transaction)
