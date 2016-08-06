# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import core.services.semestre_api


class Migration(migrations.Migration):

    dependencies = [
        ('facture', '0018_auto_20160801_2256'),
    ]

    operations = [
        migrations.AlterField(
            model_name='factureemise',
            name='semestre',
            field=models.ForeignKey(default=core.services.semestre_api.get_current_semester, to='core.Semestre', null=True),
        ),
        migrations.AlterField(
            model_name='facturerecue',
            name='semestre',
            field=models.ForeignKey(default=core.services.semestre_api.get_current_semester, to='core.Semestre', null=True),
        ),
    ]
