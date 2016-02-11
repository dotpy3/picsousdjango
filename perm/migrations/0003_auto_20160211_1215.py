# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('perm', '0002_auto_20160211_1212'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='prix',
            field=models.FloatField(default=0),
        ),
    ]
