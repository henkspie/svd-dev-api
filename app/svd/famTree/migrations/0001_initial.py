# Generated by Django 5.1.6 on 2025-02-12 08:21

import django.db.models.deletion
import famTree.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='EventList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_type', models.CharField(max_length=15, verbose_name='Event type')),
            ],
        ),
        migrations.CreateModel(
            name='Source',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('source_type', models.CharField(max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('note', models.CharField(blank=True, max_length=255)),
                ('event_type', models.CharField(choices=famTree.models.get_event_types, max_length=15)),
                ('date', models.DateField(verbose_name='Date of the event')),
                ('place', models.CharField(verbose_name='Place where the Event happened')),
                ('editor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
                ('source', models.ManyToManyField(to='famTree.source')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
