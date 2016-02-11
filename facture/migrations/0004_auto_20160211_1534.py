# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facture', '0003_auto_20160211_1117'),
    ]

    operations = [
        migrations.RenameField(
            model_name='facturerecue',
            old_name='montant_ht',
            new_name='prix',
        ),
        migrations.RenameField(
            model_name='facturerecue',
            old_name='montant_tva',
            new_name='tva',
        ),
        migrations.AlterField(
            model_name='factureemiserow',
            name='prix',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='factureemiserow',
            name='tva',
            field=models.FloatField(default=0),
        ),
    ]
