# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
from django.db import migrations
from settings import ITEM_TEMPLATE_JSON_FILE
from home_application.models import *


def initial_item_template_data(apps, schema_editor):
    try:
        json_data = open(ITEM_TEMPLATE_JSON_FILE)
        item_template_obj = json.load(json_data)
        for i in item_template_obj:
            ItemTemplate.objects.create(template_id=i['template_id'], item_id=i['item_id'])
        json_data.close()
    except Exception, e:
        print e


class Migration(migrations.Migration):
    dependencies = [
        ('home_application', '0003_initial_reports_template_data'),
    ]

    operations = [
        migrations.RunPython(initial_item_template_data),
    ]
