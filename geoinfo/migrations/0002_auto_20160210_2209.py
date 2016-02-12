# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-02-10 22:09
from __future__ import unicode_literals

import django.contrib.gis.db.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('geoinfo', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='uploader',
            options={'verbose_name_plural': 'Uploader'},
        ),
        migrations.AddField(
            model_name='polygon',
            name='is_verified',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='polygon',
            name='organizations',
            field=models.ManyToManyField(blank=True, to='claim.Organization'),
        ),
        migrations.AlterField(
            model_name='polygon',
            name='shape',
            field=django.contrib.gis.db.models.fields.PolygonField(blank=True, null=True, srid=4326),
        ),
    ]
