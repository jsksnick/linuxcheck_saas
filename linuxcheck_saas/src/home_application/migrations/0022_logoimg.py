# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home_application', '0021_checkreport_error_summary'),
    ]

    operations = [
        migrations.CreateModel(
            name='LogoImg',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('key', models.CharField(max_length=100)),
                ('value', models.BinaryField()),
            ],
        ),
    ]
