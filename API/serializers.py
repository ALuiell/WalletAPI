
from djoser.serializers import UserSerializer
from rest_framework import serializers
from .models import *
from django.utils import timezone
from django.db.models import Sum


class CustomUserSerializer(UserSerializer):
    accounts = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    bank_account_count = serializers.SerializerMethodField()  # Новое поле для количества счетов

    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + ('accounts', 'bank_account_count')

    def get_bank_account_count(self, obj):
        return obj.bank_accounts.count()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'last_login']


class BankAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankAccount
        fields = ['id', 'user', 'name', 'account_number', 'balance']
        read_only_fields = ['user', 'account_number', 'balance']


class BankAccountDetailSerializer(serializers.ModelSerializer):
    income = serializers.SerializerMethodField()
    expense = serializers.SerializerMethodField()

    class Meta:
        model = BankAccount
        fields = ['id', 'name', 'account_number', 'balance', 'income', 'expense']

    def get_income(self, obj):
        last_month = timezone.now() - timezone.timedelta(days=30)
        return Transaction.objects.filter(
            bank_account=obj,
            type='income',
            date__gte=last_month
        ).aggregate(Sum('amount'))['amount__sum'] or 0

    def get_expense(self, obj):
        last_month = timezone.now() - timezone.timedelta(days=30)
        return Transaction.objects.filter(
            bank_account=obj,
            type='expense',
            date__gte=last_month
        ).aggregate(Sum('amount'))['amount__sum'] or 0


class TransactionListSerializer(serializers.ModelSerializer):
    bank_account_number = serializers.StringRelatedField(source='bank_account.account_number', read_only=True)
    category = serializers.StringRelatedField()
    date = serializers.DateTimeField(format="%d.%m.%Y %H:%M:%S")

    class Meta:
        model = Transaction
        fields = ['id', 'uuid', 'bank_account_number', 'amount', 'description', 'category', 'type', 'date']

    def get_bank_account_number(self, obj):
        return obj.bank_account.account_number


class TransactionCreateSerializer(serializers.ModelSerializer):
    bank_account = serializers.CharField()
    category = serializers.CharField()
    date = serializers.DateTimeField(format="%d.%m.%Y %H:%M:%S", read_only=True)

    class Meta:
        model = Transaction
        fields = ['uuid', 'bank_account', 'amount', 'description', 'category', 'type', 'date']
        read_only_fields = ['date', 'uuid']

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['bank_account'] = instance.bank_account.account_number
        return ret

    def validate(self, data):
        try:
            bank_account = BankAccount.objects.get(user=self.context['request'].user,
                                                   account_number=data['bank_account'])
        except BankAccount.DoesNotExist:
            raise (
                serializers.ValidationError({"bank_account": "Bank account does not exist or does not belong to you."}))

        try:
            category = Category.objects.get(name=data['category'])
        except Category.DoesNotExist:
            raise serializers.ValidationError({"category": "Category not found."})

        if data['amount'] <= 0:
            raise serializers.ValidationError({"amount": "Amount must be positive."})
        if data['type'] not in ['income', 'expense', 'transfer']:
            raise serializers.ValidationError({"type": "Invalid transaction type."})

        data['bank_account'] = bank_account
        data['category'] = category

        return data


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']
