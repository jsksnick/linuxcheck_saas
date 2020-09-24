# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home_application', '0018_checkreport_check_task_created_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='checkreport',
            name='finish_num',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='checkreport',
            name='total_job_num',
            field=models.IntegerField(default=1),
        ),
    ]
