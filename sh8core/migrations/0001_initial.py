# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Mail',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('recipient', models.CharField(max_length=50)),
                ('secret_code', models.CharField(null=True, blank=True, max_length=16)),
                ('sender', models.CharField(max_length=200)),
                ('subject', models.CharField(max_length=400)),
                ('contents', models.TextField()),
                ('recip_date', models.DateTimeField(auto_now_add=True)),
                ('is_read', models.BooleanField(default=False)),
            ],
        ),
    ]
