# Generated by Django 3.0.4 on 2020-03-15 06:26

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SlackUserToken',
            fields=[
                ('user', models.CharField(max_length=1024, primary_key=True, serialize=False, verbose_name='Slack User ID')),
                ('token', models.CharField(max_length=1024, unique=True, verbose_name='User Access Token')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created time')),
            ],
        ),
    ]