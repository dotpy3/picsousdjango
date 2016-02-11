# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facture', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cheque',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('num', models.IntegerField()),
                ('state', models.CharField(max_length=1, choices=[(b'E', b'Encaisse'), (b'A', b'Annul\xc3\xa9'), (b'C', b'Caution')])),
                ('destinataire', models.CharField(default=None, max_length=255, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='facturerecue',
            name='cheque',
            field=models.ForeignKey(to='facture.Cheque', null=True),
        ),
    ]
