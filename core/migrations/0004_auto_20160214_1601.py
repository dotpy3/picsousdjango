# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_bugreport'),
    ]

    operations = [
        migrations.CreateModel(
            name='PeriodeTVA',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('debut', models.DateField()),
                ('fin', models.DateField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterField(
            model_name='userright',
            name='login',
            field=models.CharField(unique=True, max_length=10),
        ),
    ]
