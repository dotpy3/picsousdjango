# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facture', '0012_auto_20160313_2232'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cheque',
            name='facturerecue',
            field=models.OneToOneField(null=True, to='facture.FactureRecue'),
        ),
    ]
