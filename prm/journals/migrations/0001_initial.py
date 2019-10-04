# Generated by Django 2.2.6 on 2019-10-04 04:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('relations', '0010_delete_mood'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Mood',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, help_text='Datetime on which the object was created.', verbose_name='created at ')),
                ('modified', models.DateTimeField(auto_now=True, help_text='Datetime on which the object was last modified.', verbose_name='modified at ')),
                ('hightlights', models.CharField(blank=True, max_length=200)),
                ('mood', models.SmallIntegerField(choices=[(5, 'happy'), (4, 'good'), (3, 'neutral'), (2, 'bad'), (1, 'sad')])),
                ('description', models.TextField()),
                ('date', models.DateField()),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['date'],
                'get_latest_by': 'date',
            },
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, help_text='Datetime on which the object was created.', verbose_name='created at ')),
                ('modified', models.DateTimeField(auto_now=True, help_text='Datetime on which the object was last modified.', verbose_name='modified at ')),
                ('title', models.CharField(max_length=200)),
                ('code', django_extensions.db.fields.RandomCharField(blank=True, editable=False, length=8, unique=True)),
                ('description', models.CharField(blank=True, max_length=2000)),
                ('location', models.CharField(max_length=300)),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('contacts', models.ManyToManyField(to='relations.Contact')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created', '-modified'],
                'get_latest_by': 'created',
                'abstract': False,
            },
        ),
    ]