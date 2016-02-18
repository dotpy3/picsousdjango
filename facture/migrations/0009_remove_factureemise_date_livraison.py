# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facture', '0008_auto_20160211_1634'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='factureemise',
            name='date_livraison',
        ),
    ]
