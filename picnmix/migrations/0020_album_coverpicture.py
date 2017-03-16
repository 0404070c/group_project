# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-03-15 21:13
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('picnmix', '0019_auto_20170315_2102'),
    ]

    operations = [
        migrations.AddField(
            model_name='album',
            name='coverPicture',
            field=models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.CASCADE, to='picnmix.Photo'),
        ),
    ]