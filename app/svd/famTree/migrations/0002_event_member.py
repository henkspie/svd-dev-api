# Generated by Django 5.1.6 on 2025-02-12 11:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_member_image_alter_member_firstname'),
        ('famTree', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='member',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.member'),
        ),
    ]
