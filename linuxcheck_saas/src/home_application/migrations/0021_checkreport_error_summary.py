# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home_application', '0020_sync_check_report_info'),
    ]

    operations = [
        migrations.AddField(
            model_name='checkreport',
            name='error_summary',
            field=models.TextField(default=b'[]'),
        ),
    ]
