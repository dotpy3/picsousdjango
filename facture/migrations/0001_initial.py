# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('perm', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CategorieFactureRecue',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nom', models.CharField(max_length=255)),
                ('code', models.CharField(max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='FactureEmise',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('destinataire', models.CharField(max_length=255)),
                ('date_creation', models.DateField()),
                ('nom_createur', models.CharField(max_length=255)),
                ('date_paiement', models.DateField()),
                ('date_due', models.DateField()),
                ('etat', models.CharField(max_length=1, choices=[(b'D', b'Due'), (b'A', b'Annul\xc3\xa9e'), (b'P', b'Pay\xc3\xa9e')])),
            ],
        ),
        migrations.CreateModel(
            name='FactureEmiseRow',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nom', models.CharField(max_length=255)),
                ('prix', models.FloatField()),
                ('tva', models.FloatField()),
                ('qty', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='FactureRecue',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nom_entreprise', models.CharField(max_length=255)),
                ('date', models.DateField()),
                ('date_paiement', models.DateField(default=None, null=True)),
                ('date_remboursement', models.DateField(default=None, null=True)),
                ('moyen_paiement', models.CharField(default=None, max_length=255, null=True)),
                ('personne_a_rembourser', models.CharField(default=None, max_length=255, null=True)),
                ('montant_ht', models.FloatField(default=0)),
                ('montant_tva', models.FloatField(default=0)),
                ('immobilisation', models.BooleanField(default=False)),
                ('remarque', models.TextField(default=None, null=True)),
                ('categorie', models.ForeignKey(to='facture.CategorieFactureRecue', null=True)),
                ('perm', models.ForeignKey(default=None, to='perm.Perm', null=True)),
            ],
        ),
    ]
