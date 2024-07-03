from django.contrib import admin
from django.urls import path, include
from djoser.views import TokenCreateView

urlpatterns = [
    path("auth/", include("djoser.urls")),
    # path('accounts/'),
    # path('accounts/<int:pk>'),
]
