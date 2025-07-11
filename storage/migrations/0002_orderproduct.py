# Generated by Django 5.2 on 2025-05-13 10:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0001_initial'),
        ('storage', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=100, null=True)),
                ('brand', models.CharField(blank=True, choices=[('Sony', 'Sony'), ('X-Box', 'X-Box'), ('Nintendo', 'Nintendo')], max_length=100, null=True)),
                ('model', models.CharField(blank=True, max_length=100, null=True)),
                ('owner', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='customers.customer')),
            ],
        ),
    ]
