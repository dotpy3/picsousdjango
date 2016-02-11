# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Semestre',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('debut', models.DateField()),
                ('fin', models.DateField()),
                ('semestre', models.CharField(max_length=1, choices=[('P', 'Printemps'), ('A', 'Automne')])),
                ('annee', models.IntegerField(max_length=2)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='UserRight',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('login', models.CharField(max_length=10)),
                ('right', models.CharField(max_length=1, choices=[('A', 'Acc\xe8s total'), ('P', 'Acc\xe8s articles'), ('N', 'Acc\xe8s interdit')])),
            ],
        ),
    ]
