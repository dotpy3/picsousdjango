# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20160313_1639'),
    ]

    operations = [
        migrations.CreateModel(
            name='Semestre',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('debut', models.DateField()),
                ('fin', models.DateField()),
                ('annee', models.IntegerField(max_length=2)),
                ('periode', models.CharField(max_length=1, choices=[('A', 'Automne'), ('P', 'Printemps')])),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
