# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home_application', '0009_initial_module_item_value_data'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='module',
            name='business',
        ),
        migrations.RemoveField(
            model_name='servers',
            name='module',
        ),
        migrations.AddField(
            model_name='servers',
            name='app',
            field=models.ForeignKey(to='home_application.Business', null=True),
        ),
        migrations.DeleteModel(
            name='Module',
        ),
    ]
