# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
from django.db import migrations
from settings import CONFIG_ITEM_JSON_FILE
from home_application.models import *


def initial_config_item_data(apps, schema_editor):
    try:
        ConfigItem.objects.all().delete()
        json_data = open(CONFIG_ITEM_JSON_FILE)
        config_item_obj = json.load(json_data)
        for i in config_item_obj:
            ConfigItem.objects.create(id=i['id'], name=i['name'], field_name=i["field_name"],
                                       item_type=i["item_type"],is_deleted=i["is_deleted"])
        json_data.close()
    except Exception, e:
        print e.message


class Migration(migrations.Migration):

    dependencies = [
        ('home_application', '0006_initial_item_menu_data'),
    ]

    operations = [
        migrations.RunPython(initial_config_item_data),
    ]
