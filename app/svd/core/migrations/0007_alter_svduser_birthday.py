# Generated by Django 5.1.3 on 2024-11-13 11:26

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_alter_svduser_birthday'),
    ]

    operations = [
        migrations.AlterField(
            model_name='svduser',
            name='birthday',
            field=models.DateField(default=datetime.date(2024, 11, 13), verbose_name='Birthday of the user'),
        ),
    ]
