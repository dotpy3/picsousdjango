# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20160214_1601'),
    ]

    operations = [
        migrations.AddField(
            model_name='periodetva',
            name='state',
            field=models.CharField(default='N', max_length=1, choices=[('N', 'Non d\xe9clar\xe9e'), ('D', 'D\xe9clar\xe9e')]),
        ),
    ]
