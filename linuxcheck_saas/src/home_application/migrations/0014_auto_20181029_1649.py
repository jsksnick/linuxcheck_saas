# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home_application', '0013_auto_20181026_1658'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='checktask',
            options={'verbose_name': '\u5de1\u68c0\u4efb\u52a1'},
        ),
        migrations.AlterModelOptions(
            name='customitem',
            options={'verbose_name': '\u81ea\u5b9a\u4e49\u5de1\u68c0\u9879'},
        ),
        migrations.AlterModelOptions(
            name='mailreceiver',
            options={'verbose_name': '\u90ae\u7bb1'},
        ),
    ]
