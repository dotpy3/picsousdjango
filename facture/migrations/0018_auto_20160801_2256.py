# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_semestre'),
        ('facture', '0017_auto_20160510_1554'),
    ]

    operations = [
        migrations.AddField(
            model_name='factureemise',
            name='semestre',
            field=models.ForeignKey(to='core.Semestre', null=True),
        ),
        migrations.AddField(
            model_name='facturerecue',
            name='semestre',
            field=models.ForeignKey(to='core.Semestre', null=True),
        ),
    ]
