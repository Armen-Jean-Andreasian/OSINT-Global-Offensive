# Generated by Django 5.1.3 on 2024-12-01 09:39

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("logger_app", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="loggermodel",
            old_name="fake_url",
            new_name="destination",
        ),
        migrations.RemoveField(
            model_name="loggermodel",
            name="original_url",
        ),
        migrations.AddField(
            model_name="loggermodel",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
    ]
