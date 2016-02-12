# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20160211_1053'),
    ]

    operations = [
        migrations.CreateModel(
            name='BugReport',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('state', models.CharField(max_length=1, choices=[('N', 'Non r\xe9solu'), ('P', 'Non r\xe9solu'), ('R', 'Non r\xe9solu')])),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('reporter_name', models.CharField(max_length=255)),
                ('reporter_mail', models.CharField(max_length=255)),
                ('content', models.TextField()),
            ],
        ),
    ]
