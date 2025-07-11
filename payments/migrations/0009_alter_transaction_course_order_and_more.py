# Generated by Django 5.2.3 on 2025-06-16 12:54

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0008_remove_courseorder_user_courseorder_customer_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='course_order',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='course_order', to='payments.courseorder'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='game_order',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='game_order', to='payments.gameorder'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='order',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='order', to='payments.order'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='repair_order',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='repair_order', to='payments.repairorder'),
        ),
    ]
