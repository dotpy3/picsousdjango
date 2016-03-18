# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('perm', '0005_auto_20160212_1043'),
    ]

    operations = [
        migrations.AddField(
            model_name='perm',
            name='state',
            field=models.CharField(default=b'N', max_length=1, choices=[(b'T', b'Trait\xc3\xa9e'), (b'N', b'Non trait\xc3\xa9e')]),
        ),
    ]
