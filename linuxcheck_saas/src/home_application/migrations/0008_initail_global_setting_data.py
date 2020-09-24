# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
from django.db import migrations
from home_application.models import *


def global_setting_data(apps, schema_editor):
    try:
        GlobalSetting.objects.all().delete()
        GlobalSetting.objects.create(id=1, config_account="root", report_save=0,reports_save="30",created_by="initial_value")

    except Exception, e:
        print e.message


class Migration(migrations.Migration):

    dependencies = [
        ('home_application', '0007_initial_config_item_data'),
    ]

    operations = [
        migrations.RunPython(global_setting_data),
    ]
