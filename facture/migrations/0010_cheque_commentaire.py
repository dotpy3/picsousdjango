# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facture', '0009_remove_factureemise_date_livraison'),
    ]

    operations = [
        migrations.AddField(
            model_name='cheque',
            name='commentaire',
            field=models.TextField(default=None, null=True),
        ),
    ]
