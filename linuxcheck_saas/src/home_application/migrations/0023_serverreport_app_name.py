# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home_application', '0022_logoimg'),
    ]

    operations = [
        migrations.AddField(
            model_name='serverreport',
            name='app_name',
            field=models.CharField(default=b'', max_length=100),
        ),
    ]
