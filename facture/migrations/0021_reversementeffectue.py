# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import core.services.semestre_api


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_auto_20160801_2305'),
        ('facture', '0020_auto_20161009_0642'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReversementEffectue',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tva', models.FloatField(default=0)),
                ('prix', models.FloatField(default=0)),
                ('date_effectue', models.DateField(null=True)),
                ('semestre', models.ForeignKey(default=core.services.semestre_api.get_current_semester, to='core.Semestre', null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
