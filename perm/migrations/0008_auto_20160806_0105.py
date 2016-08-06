# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import core.services.semestre_api


class Migration(migrations.Migration):

    dependencies = [
        ('perm', '0007_perm_semestre'),
    ]

    operations = [
        migrations.AlterField(
            model_name='perm',
            name='semestre',
            field=models.ForeignKey(default=core.services.semestre_api.get_current_semester, to='core.Semestre', null=True),
        ),
    ]
