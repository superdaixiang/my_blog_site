# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2018-03-31 06:53
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20180331_1429'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articledetail',
            name='article',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='blog.Article'),
        ),
    ]