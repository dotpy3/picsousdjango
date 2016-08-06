# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_semestre'),
        ('perm', '0006_perm_state'),
    ]

    operations = [
        migrations.AddField(
            model_name='perm',
            name='semestre',
            field=models.ForeignKey(to='core.Semestre', null=True),
        ),
    ]
