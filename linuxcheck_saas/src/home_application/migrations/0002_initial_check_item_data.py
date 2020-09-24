# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
from django.db import migrations
from settings import CHECKS_ITEM_JSON_FILE
from home_application.models import *


def initial_check_item_data(apps, schema_editor):
    try:
        ItemTemplate.objects.all().delete()
        CheckItem.objects.all().delete()
        json_data = open(CHECKS_ITEM_JSON_FILE)
        check_item_obj = json.load(json_data)
        n = 1
        for i in check_item_obj:
            CheckItem.objects.create(id=n, cn_name=i['cn_name'], compare_way=i['compare_way'],
                                     enabled_change=i['enabled_change'], menu_name=i['menu_name'],
                                     name=i['name'], item_type=i["item_type"],
                                     value_type=i["value_type"], severity_level=i["severity_level"],
                                     first_menu_name=i["first_menu_name"], is_show=i["is_show"],
                                     is_selected=i["is_selected"], os_type=i["os_type"])
            n += 1
        json_data.close()
    except Exception, e:
        print e.message


class Migration(migrations.Migration):
    dependencies = [
        ('home_application', '0015_auto_20181029_1659'),
    ]

    operations = [
        migrations.RunPython(initial_check_item_data),
    ]
