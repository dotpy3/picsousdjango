# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facture', '0002_auto_20160211_1053'),
    ]

    operations = [
        migrations.AddField(
            model_name='cheque',
            name='valeur',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='factureemise',
            name='etat',
            field=models.CharField(max_length=1, choices=[(b'D', b'Due'), (b'A', b'Annul\xc3\xa9e'), (b'T', b'Partiellement pay\xc3\xa9e'), (b'P', b'Pay\xc3\xa9e')]),
        ),
    ]
