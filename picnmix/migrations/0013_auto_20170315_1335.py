# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-03-15 13:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('picnmix', '0012_auto_20170315_1319'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='image',
            field=models.ImageField(upload_to='media/'),
        ),
    ]
