# Generated by Django 3.0 on 2023-12-14 21:33

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("todo", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="user",
            name="last_login_time",
        ),
    ]
