# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home_application', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='checkitem',
            name='os_type',
            field=models.CharField(default=b'1', max_length=20),
        ),
        migrations.AddField(
            model_name='checkmodule',
            name='os_type',
            field=models.CharField(default=b'1', max_length=20),
        ),
        migrations.AddField(
            model_name='customitem',
            name='os_type',
            field=models.CharField(default=b'1', max_length=20),
        ),
        migrations.AddField(
            model_name='scriptcontent',
            name='os_type',
            field=models.CharField(default=b'1', max_length=20),
        ),
    ]
