"""
django_simple_slack_app URL Configuration
"""
from django.conf import settings
from django.urls import path
from django.views.generic import TemplateView

from django_simple_slack_app.views import SlackCommandView, SlackEventView, SlackOAuthView

event_url = getattr(settings, "SLACK_EVENT_URL", "events")
command_url = getattr(settings, "SLACK_COMMAND_URL", "command")
oauth_url = getattr(settings, "SLACK_OAUTH_URL", "oauth")

urlpatterns = [
    path(event_url, SlackEventView.as_view()),
    path(command_url, SlackCommandView.as_view()),
    path(oauth_url, SlackOAuthView.as_view()),

    path("done", TemplateView.as_view(template_name="django_simple_slack_app/oauth_done.html"), name="oauth_done"),
]
