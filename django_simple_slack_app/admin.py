from django.contrib import admin

from django_simple_slack_app.models import SlackUser, SlackTeam


@admin.register(SlackUser)
class SlackUserAdmin(admin.ModelAdmin):
    list_display = ["team", "id", "created_at"]


@admin.register(SlackTeam)
class SlackTeamAdmin(admin.ModelAdmin):
    pass
