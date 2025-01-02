# Generated by Django 5.1.4 on 2025-01-02 07:16

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("user_app", "0004_alter_usermodel_groups_alter_usermodel_last_login_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="usermodel",
            name="id",
            field=models.UUIDField(
                default=uuid.uuid4, editable=False, primary_key=True, serialize=False
            ),
        ),
    ]
