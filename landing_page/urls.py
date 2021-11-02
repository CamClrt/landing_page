"""Centralize the application urls"""

from django.urls import path
from .views import Index

app_name = "landing_page"

urlpatterns = [
    path("", Index.as_view(), name="index"),
]
