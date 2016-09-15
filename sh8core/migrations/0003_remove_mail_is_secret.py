# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sh8core', '0002_mail_is_secret'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mail',
            name='is_secret',
        ),
    ]
