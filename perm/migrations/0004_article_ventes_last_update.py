# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('perm', '0003_auto_20160211_1215'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='ventes_last_update',
            field=models.DateTimeField(default=None, null=True),
        ),
    ]
