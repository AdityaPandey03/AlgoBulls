# Generated by Django 3.0 on 2023-12-14 23:39

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("todo", "0002_remove_user_last_login_time"),
    ]

    operations = [
        migrations.AlterField(
            model_name="task",
            name="due_date",
            field=models.CharField(blank=True, max_length=40, null=True),
        ),
    ]
