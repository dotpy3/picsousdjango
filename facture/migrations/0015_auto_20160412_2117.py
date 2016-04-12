# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facture', '0014_auto_20160313_2249'),
    ]

    operations = [
        migrations.AddField(
            model_name='facturerecue',
            name='etat',
            field=models.CharField(default=b'D', max_length=1, choices=[(b'D', b'Due'), (b'A', b'Annul\xc3\xa9e'), (b'T', b'Partiellement pay\xc3\xa9e'), (b'P', b'Pay\xc3\xa9e')]),
        ),
        migrations.AlterField(
            model_name='cheque',
            name='state',
            field=models.CharField(max_length=1, choices=[(b'E', b'Encaisse'), (b'P', b'En cours'), (b'A', b'Annul\xc3\xa9'), (b'C', b'Caution')]),
        ),
    ]
