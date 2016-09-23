# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sh8core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mail',
            name='recipient',
            field=models.CharField(db_index=True, max_length=50),
        ),
    ]
