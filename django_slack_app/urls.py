"""
django_slack URL Configuration
"""
from django.conf import settings
from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from .views import SlackEventView, SlackOAuthView

oauth_url = getattr(settings, "SLACK_OAUTH_REDIRECT",  "oauth/")

urlpatterns = [
    path('', csrf_exempt(SlackEventView.as_view())),
    path(oauth_url, SlackOAuthView.as_view())
]
