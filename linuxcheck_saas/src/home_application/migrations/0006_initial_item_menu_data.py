# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
from django.db import migrations
from settings import ITEM_MENU_JSON_FILE
from home_application.models import *


def initial_item_menu_data(apps, schema_editor):
    try:
        ItemMenu.objects.all().delete()
        json_data = open(ITEM_MENU_JSON_FILE)
        item_menu_obj = json.load(json_data)
        for i in item_menu_obj:
            ItemMenu.objects.create(id=i['id'], name=i['name'], order=i['order'],child_order=i['child_order'], child_name=i['child_name'])
        json_data.close()
    except Exception, e:
        pass


class Migration(migrations.Migration):
    dependencies = [
        ('home_application', '0005_initial_script_content_data'),
    ]

    operations = [
        migrations.RunPython(initial_item_menu_data),
    ]
