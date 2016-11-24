# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sh8core', '0002_auto_20160923_2338'),
    ]

    operations = [
        migrations.AddField(
            model_name='mail',
            name='content_type',
            field=models.CharField(max_length=50, default='text/plain'),
            preserve_default=False,
        ),
    ]
