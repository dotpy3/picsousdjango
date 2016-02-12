# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('perm', '0004_article_ventes_last_update'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='perm',
            name='montantDecoHT',
        ),
        migrations.RemoveField(
            model_name='perm',
            name='montantDecoTVA',
        ),
    ]
