"""
django_slack URL Configuration
"""
from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from .views import SlackEventView


urlpatterns = [
    path('', csrf_exempt(SlackEventView.as_view())),
]
