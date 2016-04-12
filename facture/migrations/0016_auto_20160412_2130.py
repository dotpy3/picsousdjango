# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facture', '0015_auto_20160412_2117'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categoriefacturerecue',
            name='code',
            field=models.CharField(unique=True, max_length=1),
        ),
        migrations.AlterField(
            model_name='facturerecue',
            name='etat',
            field=models.CharField(default=b'D', max_length=1, choices=[(b'D', b'Due'), (b'E', b'En attente'), (b'A', b'Annul\xc3\xa9e'), (b'P', b'Pay\xc3\xa9e')]),
        ),
    ]
