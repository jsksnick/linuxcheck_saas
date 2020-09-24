# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home_application', '0014_auto_20181029_1649'),
    ]

    operations = [
        migrations.AddField(
            model_name='serverreport',
            name='source_name',
            field=models.CharField(default=b'', max_length=100),
        ),
    ]
