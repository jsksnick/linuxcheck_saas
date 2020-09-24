# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
from django.db import migrations
from settings import CONFIG_ITEM_JSON_FILE
from home_application.models import *


def initial_config_item_data(apps, schema_editor):
    try:
        reports = CheckReport.objects.all().select_related('check_task')
        if not reports.exists():
            return
        for report in reports:
            report.check_task_name = report.check_task.name
            report.check_module_id = report.check_task.check_module_id
            report.save()

    except Exception, e:
        print e.message


class Migration(migrations.Migration):

    dependencies = [
        ('home_application', '0016_auto_20181206_1612'),
    ]

    operations = [
        migrations.RunPython(initial_config_item_data),
    ]
