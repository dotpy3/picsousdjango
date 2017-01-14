# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_auto_20160801_2305'),
    ]

    operations = [
        migrations.AddField(
            model_name='semestre',
            name='solde_debut',
            field=models.IntegerField(default=0),
        ),
    ]
