# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home_application', '0024_auto_20190610_1733'),
    ]

    operations = [
        migrations.AddField(
            model_name='checkreport',
            name='total_num',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='checktask',
            name='select_type',
            field=models.CharField(default=b'ip', max_length=20),
        ),
        migrations.AddField(
            model_name='checktask',
            name='topo_list',
            field=models.TextField(default=b'[]'),
        ),
    ]
