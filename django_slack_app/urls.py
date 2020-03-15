"""
django_slack URL Configuration
"""
from django.conf import settings
from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from .views import SlackEventView, SlackOAuthView

event_url = getattr(settings, "SLACK_EVENT_URL", "events")
oauth_url = getattr(settings, "SLACK_OAUTH_URL",  "oauth")

urlpatterns = [
    path(event_url, csrf_exempt(SlackEventView.as_view())),
    path(oauth_url, csrf_exempt(SlackOAuthView.as_view()))
]
