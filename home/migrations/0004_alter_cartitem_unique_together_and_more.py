# Generated by Django 5.2 on 2025-05-25 16:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_alter_cartitem_unique_together_cartitem_colors_and_more'),
        ('storage', '0004_delete_orderproduct'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='cartitem',
            unique_together={('cart', 'product')},
        ),
        migrations.RemoveField(
            model_name='cartitem',
            name='colors',
        ),
    ]
