# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facture', '0019_auto_20160806_0105'),
    ]

    operations = [
        migrations.AddField(
            model_name='cheque',
            name='date_emission',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='cheque',
            name='date_encaissement',
            field=models.DateField(null=True),
        ),
    ]
