# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facture', '0004_auto_20160211_1534'),
    ]

    operations = [
        migrations.AlterField(
            model_name='factureemise',
            name='date_paiement',
            field=models.DateField(null=True),
        ),
    ]
