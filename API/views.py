from djoser.views import UserViewSet
from rest_framework import viewsets, generics, permissions
from .models import BankAccount, Transaction, Category
from .serializers import *
from .permissions import IsAccountOwner, IsAdminUserOrReadOnly


class UserCustomList(UserViewSet):
    serializer_class = CustomUserSerializer


class BankAccountCreateView(generics.ListCreateAPIView):
    serializer_class = BankAccountSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return BankAccount.objects.filter(user=user).prefetch_related(
            'user')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class BankAccountDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = BankAccount.objects.all()
    serializer_class = BankAccountDetailSerializer
    permission_classes = [permissions.IsAuthenticated, IsAccountOwner]

    def get_queryset(self):
        user = self.request.user
        return BankAccount.objects.filter(user=user).prefetch_related('transactions')


class TransactionListView(generics.ListAPIView):
    serializer_class = TransactionListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        account_number = self.kwargs.get('account_number')
        return Transaction.objects.filter(
            bank_account__user=user,
            bank_account__account_number=account_number)


class TransactionCreateView(generics.CreateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionCreateSerializer
    permissions_classes = [permissions.IsAuthenticated, IsAccountOwner]


class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUserOrReadOnly]


class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUserOrReadOnly]


class PostViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
