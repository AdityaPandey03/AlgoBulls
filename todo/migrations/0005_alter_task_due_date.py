# Generated by Django 4.2 on 2023-12-16 17:03

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("todo", "0004_alter_task_user"),
    ]

    operations = [
        migrations.AlterField(
            model_name="task",
            name="due_date",
            field=models.DateField(blank=True, max_length=40, null=True),
        ),
    ]