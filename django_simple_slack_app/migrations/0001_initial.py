# Generated by Django 3.0.4 on 2020-06-28 11:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SlackTeam',
            fields=[
                ('id', models.CharField(max_length=64, primary_key=True, serialize=False, verbose_name='Team Slack-ID')),
                ('name', models.CharField(max_length=1024, null=True, verbose_name='Team Name')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='created time')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created time')),
            ],
        ),
        migrations.CreateModel(
            name='SlackUser',
            fields=[
                ('id', models.CharField(max_length=64, primary_key=True, serialize=False, verbose_name='User Slack-ID')),
                ('token', models.CharField(max_length=1024, unique=True, verbose_name='User Access Token')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='created time')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created time')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='django_simple_slack_app.SlackTeam')),
            ],
        ),
    ]
