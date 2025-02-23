# Generated by Django 5.1.3 on 2024-11-15 06:25

import datetime
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("logger_app", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="ObtainedDataModel",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date_time", models.DateTimeField(default=datetime.datetime.utcnow)),
                ("ip", models.CharField(db_index=True, max_length=45)),
                ("browser", models.CharField(blank=True, max_length=100, null=True)),
                (
                    "operating_system",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                ("user_agent", models.CharField(blank=True, max_length=255, null=True)),
                ("host_name", models.CharField(blank=True, max_length=255, null=True)),
                ("isp", models.CharField(blank=True, max_length=100, null=True)),
                (
                    "logger",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="obtained_datas",
                        to="logger_app.loggermodel",
                    ),
                ),
            ],
        ),
    ]
