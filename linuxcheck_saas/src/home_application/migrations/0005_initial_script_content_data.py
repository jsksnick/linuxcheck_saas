# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
from django.db import migrations
from settings import SCRIPTS_CHECK_FILE,SCRIPTS_CHECK_CONFIG_INFO_FILE,SCRIPTS_PERFORMS_FILE,SCRIPTS_SERVER_INFO_FILE, SCRIPTS_SUSE_CHECK_FILE, SCRIPTS_SUSE_PERFORMS_FILE
from home_application.models import *


def initial_script_content_data(apps, schema_editor):
    try:
        ScriptContent.objects.all().delete()
        file_data1 = file(SCRIPTS_CHECK_FILE)
        ScriptContent.objects.create(os_type="1", name="check", description="服务器检查脚本", content=file_data1.read())
        file_data1.close()
        file_data2 = file(SCRIPTS_PERFORMS_FILE)
        ScriptContent.objects.create(os_type="1", name="performs", description="服务器性能信息收集脚本", content=file_data2.read())
        file_data2.close()
        file_data3 = file(SCRIPTS_SERVER_INFO_FILE)
        ScriptContent.objects.create(os_type="1", name="servers_info", description="服务器主机和系统信息获取脚本", content=file_data3.read())
        file_data3.close()
        file_data4 = file(SCRIPTS_CHECK_CONFIG_INFO_FILE)
        ScriptContent.objects.create(os_type="1", name="config_info", description="配置信息收集脚本", content=file_data4.read())
        file_data4.close()
        file_data5 = file(SCRIPTS_SUSE_CHECK_FILE)
        ScriptContent.objects.create(os_type="2", name="check", description="服务器检查脚本", content=file_data5.read())
        file_data5.close()
        file_data6 = file(SCRIPTS_SUSE_PERFORMS_FILE)
        ScriptContent.objects.create(os_type="2", name="performs", description="服务器性能信息收集脚本", content=file_data6.read())
        file_data6.close()
    except Exception, e:
        pass


class Migration(migrations.Migration):
    dependencies = [
        ('home_application', '0004_initial_item_template_data'),
    ]

    operations = [
        migrations.RunPython(initial_script_content_data),
    ]
