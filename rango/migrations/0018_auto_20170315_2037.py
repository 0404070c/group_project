# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-03-15 20:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rango', '0017_album_coverpicture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='album',
            name='coverPicture',
            field=models.ImageField(blank=True, default='', null=True, upload_to=b''),
        ),
    ]
