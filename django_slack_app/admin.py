from django.contrib import admin

from django_slack_app.models import SlackUserToken


@admin.register(SlackUserToken)
class SlackUserTokenAdmin(admin.ModelAdmin):
    list_display = ["team_name", "user", "created_at"]
