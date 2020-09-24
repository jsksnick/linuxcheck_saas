# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home_application', '0015_serverreport_source_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='checkreport',
            name='check_module',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='home_application.CheckModule', null=True),
        ),
        migrations.AddField(
            model_name='checkreport',
            name='check_task_name',
            field=models.CharField(default=b'', max_length=100),
        ),
        migrations.AlterField(
            model_name='checkreport',
            name='check_task',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to='home_application.CheckTask', null=True),
        ),
    ]
