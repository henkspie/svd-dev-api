# Generated by Django 5.1.2 on 2024-11-04 07:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_member'),
    ]

    operations = [
        migrations.RenameField(
            model_name='member',
            old_name='birth_gender',
            new_name='sex',
        ),
        migrations.RemoveField(
            model_name='member',
            name='death_date',
        ),
        migrations.RemoveField(
            model_name='member',
            name='death_date_txt',
        ),
        migrations.RemoveField(
            model_name='member',
            name='time_birth',
        ),
    ]
