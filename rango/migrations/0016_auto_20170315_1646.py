# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-03-15 16:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rango', '0015_auto_20170315_1643'),
    ]

    operations = [
        migrations.AlterField(
            model_name='album',
            name='sharedUsers',
            field=models.CharField(blank=True, default='', max_length=2048, null=True),
        ),
    ]