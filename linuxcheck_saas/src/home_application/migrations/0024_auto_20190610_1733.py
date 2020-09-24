# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home_application', '0023_serverreport_app_name'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='checkreport',
            options={'verbose_name': '\u5de1\u68c0\u62a5\u544a'},
        ),
        migrations.AddField(
            model_name='checkreport',
            name='server_num',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='checktask',
            name='group_list',
            field=models.TextField(default=b'[]'),
        ),
    ]
