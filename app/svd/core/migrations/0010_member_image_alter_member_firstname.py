# Generated by Django 5.1.4 on 2025-01-13 16:56

import core.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_alter_member_editor_alter_member_father_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='image',
            field=models.ImageField(null=True, upload_to=core.models.member_image_filepath),
        ),
        migrations.AlterField(
            model_name='member',
            name='firstname',
            field=models.CharField(help_text='The first name(s) as stated in your passport or ID-card or given at birth', max_length=63, verbose_name='First name(s)'),
        ),
    ]
