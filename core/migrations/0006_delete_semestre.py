# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_periodetva_state'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Semestre',
        ),
    ]
