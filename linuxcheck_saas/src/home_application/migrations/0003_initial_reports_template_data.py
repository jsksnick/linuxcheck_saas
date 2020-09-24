# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
from django.db import migrations
from settings import REPORTS_TEMPLATE_JSON_FILE
from home_application.models import *


def initial_reports_template_data(apps, schema_editor):
    try:
        ReportsTemplate.objects.all().delete()
        json_data = open(REPORTS_TEMPLATE_JSON_FILE)
        reports_template_obj = json.load(json_data)
        n = 1
        for i in reports_template_obj:
            ReportsTemplate.objects.create(id=n, name=i['name'], description=i['description'])
            n += 1
        json_data.close()
    except Exception, e:
        pass


class Migration(migrations.Migration):

    dependencies = [
        ('home_application', '0002_initial_check_item_data'),
    ]

    operations = [
        migrations.RunPython(initial_reports_template_data),
    ]
