"""Module for routing urls."""
from django.urls import path, include

from . import views

urlpatterns = [
    path("", views.home_page_view, name="home"),
    path("database_test/", views.database_test_view, name="database_test"),
    path("accounts/", include("django.contrib.auth.urls")),
]
