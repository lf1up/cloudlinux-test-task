# Generated by Django 5.2 on 2025-04-05 01:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("appointments", "0002_rename_response_response_text"),
    ]

    operations = [
        migrations.AlterField(
            model_name="appointment",
            name="date",
            field=models.DateField(auto_created=True, blank=True, null=True),
        ),
    ]
