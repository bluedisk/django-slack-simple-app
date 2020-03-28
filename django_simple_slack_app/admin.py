from django.contrib import admin

from django_simple_slack_app.models import SlackUser


@admin.register(SlackUser)
class SlackUserAdmin(admin.ModelAdmin):
    list_display = ["team_name", "user", "created_at"]
