# Generated by Django 5.2 on 2025-05-26 19:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_blogcategory_blogpost'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpost',
            name='author',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
