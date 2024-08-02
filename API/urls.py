from django.urls import path, include
from .views import *

urlpatterns = [
    path("auth/", include("djoser.urls")),
    path('auth/', include('djoser.urls.authtoken')),
    # path('auth/', include('djoser.urls.jwt')),
    path('accounts', BankAccountCreateView.as_view(), name='bank_account'),
    path('accounts/detail/<int:pk>', BankAccountDetailView.as_view(), name='detail_bank_account'),
    path('transactions/<str:account_number>', TransactionListView.as_view(), name='transaction_list'),
    path('transactions/create/', TransactionCreateView.as_view(), name='transaction_create'),
    path('category', CategoryListCreateView.as_view(), name='category_create'),
    path('category/<int:pk>', CategoryDetailView.as_view(), name='category_detail'),
]
