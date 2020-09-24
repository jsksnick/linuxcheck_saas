# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Business',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('created_by', models.CharField(max_length=100)),
                ('when_created', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='CeleryTimeSet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_time', models.CharField(max_length=100)),
                ('run_time', models.CharField(max_length=100)),
                ('time_interval', models.IntegerField(default=0)),
                ('time_type', models.CharField(max_length=10)),
                ('is_deleted', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='CheckItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cn_name', models.CharField(max_length=100)),
                ('compare_way', models.CharField(default=None, max_length=100, null=True)),
                ('enabled_change', models.BooleanField(default=False)),
                ('menu_name', models.CharField(default=None, max_length=100, null=True)),
                ('name', models.CharField(max_length=100)),
                ('item_type', models.CharField(max_length=10)),
                ('value_type', models.CharField(default=None, max_length=10, null=True)),
                ('severity_level', models.CharField(default=None, max_length=10, null=True)),
                ('first_menu_name', models.CharField(default=None, max_length=100, null=True)),
                ('is_show', models.BooleanField(default=True)),
                ('is_selected', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='CheckItemValue',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.TextField()),
                ('check_item', models.ForeignKey(to='home_application.CheckItem')),
            ],
        ),
        migrations.CreateModel(
            name='CheckModule',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('when_created', models.CharField(max_length=30)),
                ('created_by', models.CharField(max_length=100)),
                ('modified_by', models.CharField(default=b'', max_length=100)),
                ('when_modified', models.CharField(default=b'', max_length=30)),
                ('base_module_id', models.IntegerField(default=0)),
                ('is_build_in', models.BooleanField(default=False)),
                ('is_deleted', models.BooleanField(default=False)),
                ('description', models.TextField(default=b'')),
            ],
        ),
        migrations.CreateModel(
            name='CheckReport',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('when_created', models.CharField(max_length=100)),
                ('report_info', models.CharField(max_length=200, null=True)),
                ('status', models.CharField(default=b'RUNNING', max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='CheckTask',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('created_by', models.CharField(max_length=100)),
                ('ip_list', models.TextField()),
                ('is_deleted', models.BooleanField(default=False)),
                ('modified_by', models.CharField(default=b'', max_length=100)),
                ('receivers', models.TextField()),
                ('script_account', models.CharField(max_length=100)),
                ('when_created', models.CharField(max_length=100)),
                ('when_modified', models.CharField(default=b'', max_length=100)),
                ('celery_time_set', models.OneToOneField(to='home_application.CeleryTimeSet')),
                ('check_module', models.ForeignKey(to='home_application.CheckModule')),
            ],
        ),
        migrations.CreateModel(
            name='ConfigInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.TextField(null=True)),
                ('is_delete', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='ConfigItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.TextField(max_length=500, null=True)),
                ('field_name', models.TextField(max_length=500, null=True)),
                ('item_type', models.CharField(max_length=100, null=True)),
                ('value_type', models.CharField(max_length=100, null=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('is_build_in', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='ConfigServer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('when_created', models.CharField(max_length=100)),
                ('is_delete', models.BooleanField(default=False)),
                ('created_by', models.CharField(max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='CustomInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.TextField()),
                ('config_item', models.ForeignKey(to='home_application.ConfigItem')),
            ],
        ),
        migrations.CreateModel(
            name='CustomItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('cn_name', models.CharField(max_length=100)),
                ('description', models.TextField(default=b'', null=True)),
                ('script_content', models.TextField()),
                ('created_by', models.CharField(max_length=100)),
                ('when_created', models.CharField(max_length=30)),
                ('when_modified', models.CharField(default=b'', max_length=30)),
                ('compare_way', models.CharField(max_length=10)),
                ('compare_value', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='CustomItemValue',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.TextField()),
                ('check_module', models.ForeignKey(to='home_application.CheckModule')),
                ('custom_item', models.ForeignKey(to='home_application.CustomItem')),
            ],
        ),
        migrations.CreateModel(
            name='CustomReportDetail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.TextField()),
                ('is_warn', models.BooleanField(default=False)),
                ('custom_item', models.ForeignKey(to='home_application.CustomItem')),
            ],
        ),
        migrations.CreateModel(
            name='GlobalSetting',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('config_account', models.CharField(max_length=100, null=True)),
                ('report_save', models.IntegerField(default=0, null=True)),
                ('reports_save', models.CharField(max_length=100, null=True)),
                ('created_by', models.CharField(max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ItemMenu',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('child_name', models.CharField(max_length=100, null=True)),
                ('order', models.IntegerField()),
                ('child_order', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='ItemTemplate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('item', models.ForeignKey(to='home_application.CheckItem')),
            ],
        ),
        migrations.CreateModel(
            name='MailReceiver',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('account', models.CharField(max_length=100)),
                ('mailbox', models.CharField(max_length=50)),
                ('when_created', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Module',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('business', models.ForeignKey(to='home_application.Business')),
            ],
        ),
        migrations.CreateModel(
            name='OperationLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('operator', models.CharField(max_length=100, null=True)),
                ('operated_type', models.TextField(max_length=100)),
                ('operated_detail', models.TextField(max_length=1000)),
                ('when_created', models.CharField(max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ReportsSubscibe',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('created_by', models.CharField(max_length=100)),
                ('ip_list', models.TextField()),
                ('is_deleted', models.BooleanField(default=False)),
                ('modified_by', models.CharField(max_length=100)),
                ('receivers', models.TextField()),
                ('when_created', models.CharField(default=None, max_length=100, null=True)),
                ('when_modified', models.CharField(default=None, max_length=100, null=True)),
                ('when_start', models.CharField(default=None, max_length=100, null=True)),
                ('when_end', models.CharField(default=None, max_length=100, null=True)),
                ('time_type', models.CharField(max_length=100, null=True)),
                ('time_interval', models.IntegerField(default=None, null=True)),
                ('celery_time_set', models.OneToOneField(null=True, default=None, to='home_application.CeleryTimeSet')),
            ],
        ),
        migrations.CreateModel(
            name='ReportsTemplate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.CharField(default=None, max_length=100, null=True)),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='ScriptContent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('content', models.TextField()),
                ('description', models.CharField(default=None, max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ServerReport',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ip_address', models.CharField(max_length=50)),
                ('app_id', models.IntegerField()),
                ('source', models.IntegerField()),
                ('is_success', models.BooleanField(default=True)),
                ('summary', models.TextField(default=b'')),
                ('check_report', models.ForeignKey(to='home_application.CheckReport')),
            ],
        ),
        migrations.CreateModel(
            name='ServerReportDetail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.TextField()),
                ('warn_status', models.BooleanField(default=False)),
                ('check_item', models.ForeignKey(default=None, to='home_application.CheckItem', null=True)),
                ('server_report', models.ForeignKey(to='home_application.ServerReport')),
            ],
        ),
        migrations.CreateModel(
            name='Servers',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ip', models.CharField(max_length=100)),
                ('host_name', models.CharField(default=b'', max_length=100, null=True)),
                ('operation_system', models.CharField(default=b'', max_length=200, null=True)),
                ('source', models.CharField(max_length=100, null=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('module', models.ForeignKey(to='home_application.Module', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='SubscibeDetail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.TextField()),
                ('when_created', models.CharField(max_length=100)),
                ('check_item', models.ForeignKey(to='home_application.CheckItem')),
                ('server_report', models.ForeignKey(to='home_application.ServerReport', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='SysConfig',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('key', models.CharField(max_length=100)),
                ('value', models.TextField()),
            ],
        ),
        migrations.AddField(
            model_name='reportssubscibe',
            name='reports_template',
            field=models.ForeignKey(to='home_application.ReportsTemplate'),
        ),
        migrations.AddField(
            model_name='itemtemplate',
            name='template',
            field=models.ForeignKey(to='home_application.ReportsTemplate'),
        ),
        migrations.AddField(
            model_name='customreportdetail',
            name='server_report',
            field=models.ForeignKey(to='home_application.ServerReport'),
        ),
        migrations.AddField(
            model_name='custominfo',
            name='server',
            field=models.ForeignKey(to='home_application.Servers'),
        ),
        migrations.AddField(
            model_name='configserver',
            name='server',
            field=models.ForeignKey(to='home_application.Servers', null=True),
        ),
        migrations.AddField(
            model_name='configinfo',
            name='config_item',
            field=models.ForeignKey(to='home_application.ConfigItem', null=True),
        ),
        migrations.AddField(
            model_name='configinfo',
            name='server_ip',
            field=models.ForeignKey(to='home_application.ConfigServer', null=True),
        ),
        migrations.AddField(
            model_name='checkreport',
            name='check_task',
            field=models.ForeignKey(to='home_application.CheckTask'),
        ),
        migrations.AddField(
            model_name='checkitemvalue',
            name='check_module',
            field=models.ForeignKey(to='home_application.CheckModule'),
        ),
    ]
