# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home_application', '0012_subscibedetail_is_warn'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='checkmodule',
            options={'verbose_name': '\u81ea\u5b9a\u4e49\u6a21\u677f'},
        ),
        migrations.RenameField(
            model_name='operationlog',
            old_name='operated_type',
            new_name='operate_type',
        ),
        migrations.RemoveField(
            model_name='operationlog',
            name='operated_detail',
        ),
        migrations.AddField(
            model_name='operationlog',
            name='operate_detail',
            field=models.TextField(default=b''),
        ),
        migrations.AddField(
            model_name='operationlog',
            name='operate_obj',
            field=models.CharField(default=b'', max_length=100),
        ),
        migrations.AddField(
            model_name='operationlog',
            name='operate_summary',
            field=models.TextField(default=b''),
        ),
    ]
