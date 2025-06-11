from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0004_employeefile'),
    ]

    operations = [
        migrations.AddField(
            model_name='employeetask',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
    ]
