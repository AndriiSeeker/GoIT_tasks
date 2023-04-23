from django.urls import path

from . import views

app_name = "quotes"

urlpatterns = [
    path("", views.home, name='home'),
    path("quotes/", views.home, name='home'),
    path("<int:page>", views.home, name='home_paginate'),
    path("quote/", views.quote, name='add_quote'),
]
