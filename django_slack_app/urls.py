"""
django_slack URL Configuration
"""
from django.conf import settings
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView

from .views import SlackEventView, SlackOAuthView

event_url = getattr(settings, "SLACK_EVENT_URL", "events")
oauth_url = getattr(settings, "SLACK_OAUTH_URL",  "oauth")

urlpatterns = [
    path(event_url, csrf_exempt(SlackEventView.as_view())),
    path(oauth_url, csrf_exempt(SlackOAuthView.as_view())),

    path("done", TemplateView.as_view(template_name="slack_app/oauth_done.html"), name="oauth_done"),
]
