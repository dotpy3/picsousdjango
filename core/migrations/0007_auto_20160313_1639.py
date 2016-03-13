# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_delete_semestre'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bugreport',
            name='state',
            field=models.CharField(max_length=1, choices=[('N', 'Non r\xe9solu'), ('P', 'En cours'), ('R', 'Termin\xe9')]),
        ),
    ]
