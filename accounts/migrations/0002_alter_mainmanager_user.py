# Generated by Django 5.2.3 on 2025-07-02 08:59

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mainmanager',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='main_manager', to=settings.AUTH_USER_MODEL),
        ),
    ]
