# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations
from home_application.models import *


def initial_config_item_data(apps, schema_editor):
    try:
        reports = CheckReport.objects.all().select_related('check_task')
        if not reports.exists():
            return
        for report in reports:
            if not report.check_task:
                continue
            report.check_task_name = report.check_task.name
            report.check_module_id = report.check_task.check_module_id
            report.check_task_created_by = report.check_task.created_by
            report.save()

    except Exception, e:
        print e.message


class Migration(migrations.Migration):

    dependencies = [
        ('home_application', '0019_auto_20181211_1049'),
    ]

    operations = [
        migrations.RunPython(initial_config_item_data),
    ]
