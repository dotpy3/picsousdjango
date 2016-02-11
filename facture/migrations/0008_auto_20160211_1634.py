# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facture', '0007_merge'),
    ]

    operations = [
        migrations.AddField(
            model_name='factureemise',
            name='date_livraison',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='factureemise',
            name='date_creation',
            field=models.DateField(auto_now_add=True),
        ),
    ]
