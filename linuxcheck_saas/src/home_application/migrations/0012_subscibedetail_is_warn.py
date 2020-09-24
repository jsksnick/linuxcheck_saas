# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home_application', '0011_mailreceiver_created_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscibedetail',
            name='is_warn',
            field=models.BooleanField(default=False),
        ),
    ]
