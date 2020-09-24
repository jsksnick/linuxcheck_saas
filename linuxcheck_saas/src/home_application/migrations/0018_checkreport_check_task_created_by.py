# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models

from home_application.models import *


def initial_config_item_data(apps, schema_editor):
    try:
        reports = CheckReport.objects.all().select_related('check_task')
        if not reports.exists():
            return
        for report in reports:
            report.check_task_created_by = report.check_task.created_by
            report.save()

    except Exception, e:
        print e.message


class Migration(migrations.Migration):

    dependencies = [
        ('home_application', '0017_sync_check_task_info'),
    ]

    operations = [
        migrations.AddField(
            model_name='checkreport',
            name='check_task_created_by',
            field=models.CharField(default=b'', max_length=100),
        ),
        migrations.RunPython(initial_config_item_data),
    ]
