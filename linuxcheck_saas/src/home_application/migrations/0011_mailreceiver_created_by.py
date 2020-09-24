# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home_application', '0010_auto_20180609_1736'),
    ]

    operations = [
        migrations.AddField(
            model_name='mailreceiver',
            name='created_by',
            field=models.CharField(default=b'', max_length=100),
        ),
    ]
