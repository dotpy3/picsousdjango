# coding: utf8
#
from __future__ import unicode_literals

from django.db import models

class UserRight(models.Model):
    USERRIGHT_ALL = 'A'
    USERRIGHT_ARTICLES = 'P'
    USERRIGHT_NONE = 'N'

    USERRIGHT_CHOICES = (
        (USERRIGHT_ALL, 'Accès total'),
        (USERRIGHT_ARTICLES, 'Accès articles'),
        (USERRIGHT_NONE, 'Accès interdit'),
    )

    login = models.CharField(max_length=10)
    right = models.CharField(max_length=1, choices=USERRIGHT_CHOICES)


class Periode(models.Model):
    debut = models.DateField()
    fin = models.DateField()

    class Meta:
        abstract = True


class Semestre(Periode):
    SEMESTRE_PRINTEMPS = 'P'
    SEMESTRE_AUTOMNE = 'A'

    SEMESTRE_CHOICES = (
        (SEMESTRE_PRINTEMPS, 'Printemps'),
        (SEMESTRE_AUTOMNE, 'Automne'),
    )

    semestre = models.CharField(max_length=1, choices=SEMESTRE_CHOICES)
    annee = models.IntegerField()
