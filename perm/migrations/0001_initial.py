# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('id_payutc', models.IntegerField(default=None, null=True)),
                ('stock', models.IntegerField(default=0)),
                ('ventes', models.IntegerField(default=0)),
                ('tva', models.FloatField(default=0)),
                ('prix', models.IntegerField(default=0)),
                ('nom', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Perm',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nom', models.CharField(max_length=255)),
                ('asso', models.BooleanField(default=True)),
                ('nom_resp', models.CharField(default=None, max_length=255, null=True)),
                ('mail_resp', models.CharField(default=None, max_length=255, null=True)),
                ('tel_resp', models.CharField(default=None, max_length=255, null=True)),
                ('role', models.CharField(default=None, max_length=255, null=True)),
                ('date', models.DateField()),
                ('periode', models.CharField(max_length=1, choices=[(b'M', b'Matin'), (b'D', b'Midi'), (b'S', b'Soir')])),
                ('montantTTCMaxAutorise', models.FloatField(default=None, null=True)),
                ('montantDecoHT', models.FloatField(default=0)),
                ('montantDecoTVA', models.FloatField(default=0)),
                ('remarque', models.TextField(default=None, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='article',
            name='perm',
            field=models.ForeignKey(to='perm.Perm'),
        ),
    ]
