# Generated by Django 5.1.3 on 2024-11-15 06:36

import django.contrib.auth.models
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
        ("user_app", "0002_usermodel_salt"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="usermodel",
            options={"verbose_name": "user", "verbose_name_plural": "users"},
        ),
        migrations.AlterModelManagers(
            name="usermodel",
            managers=[
                ("objects", django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.AddField(
            model_name="usermodel",
            name="date_joined",
            field=models.DateTimeField(
                default=django.utils.timezone.now, verbose_name="date joined"
            ),
        ),
        migrations.AddField(
            model_name="usermodel",
            name="email",
            field=models.EmailField(
                blank=True, max_length=254, verbose_name="email address"
            ),
        ),
        migrations.AddField(
            model_name="usermodel",
            name="first_name",
            field=models.CharField(
                blank=True, max_length=150, verbose_name="first name"
            ),
        ),
        migrations.AddField(
            model_name="usermodel",
            name="groups",
            field=models.ManyToManyField(
                blank=True, related_name="user_app_user_set", to="auth.group"
            ),
        ),
        migrations.AddField(
            model_name="usermodel",
            name="is_active",
            field=models.BooleanField(
                default=True,
                help_text="Designates whether this user should be treated as active. Unselect this instead of deleting accounts.",
                verbose_name="active",
            ),
        ),
        migrations.AddField(
            model_name="usermodel",
            name="is_staff",
            field=models.BooleanField(
                default=False,
                help_text="Designates whether the user can log into this admin site.",
                verbose_name="staff status",
            ),
        ),
        migrations.AddField(
            model_name="usermodel",
            name="is_superuser",
            field=models.BooleanField(
                default=False,
                help_text="Designates that this user has all permissions without explicitly assigning them.",
                verbose_name="superuser status",
            ),
        ),
        migrations.AddField(
            model_name="usermodel",
            name="last_login",
            field=models.DateTimeField(
                blank=True, default=django.utils.timezone.now, null=True
            ),
        ),
        migrations.AddField(
            model_name="usermodel",
            name="last_name",
            field=models.CharField(
                blank=True, max_length=150, verbose_name="last name"
            ),
        ),
        migrations.AddField(
            model_name="usermodel",
            name="user_permissions",
            field=models.ManyToManyField(
                blank=True, related_name="user_app_permission_set", to="auth.permission"
            ),
        ),
        migrations.AlterField(
            model_name="usermodel",
            name="salt",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
