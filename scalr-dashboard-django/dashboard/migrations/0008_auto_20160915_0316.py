# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-09-15 03:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0007_auto_20160915_0307'),
    ]

    operations = [
        migrations.AlterField(
            model_name='farms',
            name='f_dis',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='farmsroles',
            name='fname',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='farmsroles',
            name='r_alias',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='farmsroles',
            name='r_name',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]
