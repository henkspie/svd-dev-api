# Generated by Django 5.1.2 on 2024-10-27 09:32

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_alter_svduser_email'),
    ]

    operations = [
        migrations.CreateModel(
            name='Member',
            fields=[
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('note', models.CharField(blank=True, max_length=255)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('firstname', models.CharField(help_text='The first name(s) as stated in your passport or ID-card or given at birth', max_length=63, verbose_name='First name')),
                ('lastname', models.CharField(max_length=63, verbose_name='Last Name')),
                ('call_name', models.CharField(blank=True, max_length=15, verbose_name='Call name')),
                ('birth_gender', models.CharField(choices=[('U', 'Unassigned'), ('M', 'Man'), ('F', 'Female')], db_comment='Can be UNASSIGNED, MAN or FEMALE.', default='U', help_text='A modern choice is Unassigned', max_length=3, verbose_name='Gender by birth')),
                ('birthday', models.DateField(blank=True, help_text='Please use the following format: <em><strong>YYYY-MM-DD</strong><em>.', null=True, verbose_name='Date of Birth')),
                ('time_birth', models.TimeField(blank=True, help_text='Please use the following format: <em><strong>14:00:00</strong><em>.', null=True, verbose_name='Time of Birth')),
                ('birthday_txt', models.CharField(blank=True, max_length=16, null=True)),
                ('death_date', models.DateField(blank=True, help_text='Please use the following format: <em><strong>YYYY-MM-DD</strong></em>.', null=True, verbose_name='Died')),
                ('death_date_txt', models.CharField(blank=True, max_length=16, null=True)),
                ('editor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('father', models.ForeignKey(blank=True, help_text='If not known leave it blank!', limit_choices_to={'birth_gender': 'M'}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_query_name='bio_father', to='core.member', verbose_name='Biological father')),
                ('mother', models.ForeignKey(blank=True, help_text='If not known leave it blank!', limit_choices_to={'birth_gender': 'F'}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='bio_mother', to='core.member', verbose_name='Biological mother')),
            ],
            options={
                'ordering': ['-birthday_txt', 'lastname'],
            },
        ),
    ]
