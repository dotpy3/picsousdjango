# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facture', '0010_cheque_commentaire'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='facturerecue',
            name='cheque',
        ),
        migrations.AddField(
            model_name='cheque',
            name='cheque',
            field=models.ForeignKey(to='facture.FactureRecue', null=True),
        ),
    ]
