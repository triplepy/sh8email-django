# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sh8core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='mail',
            name='is_secret',
            field=models.BooleanField(default=False),
        ),
    ]
