# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-10 20:26
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('albion', '0004_auto_20170809_2341'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='playercraft',
            name='user',
        ),
        migrations.AddField(
            model_name='albioncharacter',
            name='discord',
            field=models.CharField(default=None, max_length=32),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='playercraft',
            name='character',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='albion.AlbionCharacter'),
            preserve_default=False,
        ),
    ]