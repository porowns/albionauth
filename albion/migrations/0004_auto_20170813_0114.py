# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-13 01:14
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('albion', '0003_static'),
    ]

    operations = [
        migrations.AlterField(
            model_name='static',
            name='leader',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='leader', to='albion.AlbionCharacter'),
        ),
        migrations.AlterField(
            model_name='static',
            name='members',
            field=models.ManyToManyField(blank=True, null=True, to='albion.AlbionCharacter'),
        ),
    ]
