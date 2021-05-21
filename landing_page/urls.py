"""Centralize the application urls"""

from django.urls import path

from . import views

app_name = "landing_page"

urlpatterns = [
    path(
        "",
        views.index,
        name="index",
    ),
]
