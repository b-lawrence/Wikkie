# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-05 10:55
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('wiki', '0003_auto_20160504_0957'),
    ]

    operations = [
        migrations.CreateModel(
            name='PageVersion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('version', models.IntegerField()),
                ('title', models.CharField(max_length=50)),
                ('content', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='page',
            name='author',
        ),
        migrations.RemoveField(
            model_name='page',
            name='content',
        ),
        migrations.RemoveField(
            model_name='page',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='page',
            name='title',
        ),
        migrations.RemoveField(
            model_name='page',
            name='updated_at',
        ),
        migrations.AddField(
            model_name='pageversion',
            name='page',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wiki.Page'),
        ),
    ]
