# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2018-03-31 06:29
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20180320_1935'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Verify',
        ),
        migrations.RemoveField(
            model_name='articledetail',
            name='summery',
        ),
    ]
