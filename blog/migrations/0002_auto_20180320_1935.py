# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2018-03-20 11:35
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='article',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='author',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='reply_to',
        ),
        migrations.RemoveField(
            model_name='article',
            name='cont_comment',
        ),
        migrations.RemoveField(
            model_name='article',
            name='summery',
        ),
        migrations.DeleteModel(
            name='Comment',
        ),
    ]
