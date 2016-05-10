# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facture', '0016_auto_20160412_2130'),
    ]

    operations = [
        migrations.AlterField(
            model_name='facturerecue',
            name='etat',
            field=models.CharField(default=b'D', max_length=1, choices=[(b'D', b'\xc3\x80 payer'), (b'R', b'\xc3\x80 rembourser'), (b'E', b'En attente'), (b'P', b'Pay\xc3\xa9e')]),
        ),
    ]
