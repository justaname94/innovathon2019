# Generated by Django 2.2.6 on 2019-10-04 16:33

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('journals', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='event',
            old_name='time',
            new_name='end_time',
        ),
        migrations.AddField(
            model_name='event',
            name='start_time',
            field=models.TimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
