# Generated by Django 5.1.3 on 2024-11-13 11:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_svduser_birthday_svduser_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='svduser',
            name='birthday',
            field=models.DateField(blank=True, verbose_name='Birthday of the user'),
        ),
    ]
