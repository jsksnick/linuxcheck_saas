# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.9 Stackless 3.1b3 060516 (default, Nov 28 2016, 09:05:13) 
# [GCC 4.4.7 20120313 (Red Hat 4.4.7-17)]
# Embedded file name: /bkdata/vcs2/tmp/linuxcheck_saas-1561098846.95/linuxcheck_saas/src/home_application/models.py
# Compiled at: 2019-06-21 14:34:36
import json, datetime
from django.db import models
TimeType = {'now': u'\u7acb\u5373', 
   'cycle': u'\u5468\u671f', 
   'time': u'\u5b9a\u65f6'}

class Business(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    created_by = models.CharField(max_length=100)
    when_created = models.CharField(max_length=100)

    def to_dic(self):
        return dict([ (attr, getattr(self, attr)) for attr in [ f.name for f in self._meta.fields ] ])


class ConfigItem(models.Model):
    name = models.TextField(max_length=500, null=True)
    field_name = models.TextField(max_length=500, null=True)
    item_type = models.CharField(max_length=100, null=True)
    value_type = models.CharField(max_length=100, null=True)
    is_deleted = models.BooleanField(default=False)
    is_build_in = models.BooleanField(default=True)

    def to_dic(self):
        return dict([ (attr, getattr(self, attr)) for attr in [ f.name for f in self._meta.fields ] ])


class Servers(models.Model):
    app = models.ForeignKey(Business, null=True)
    ip = models.CharField(max_length=100)
    host_name = models.CharField(max_length=100, null=True, default='')
    operation_system = models.CharField(max_length=200, null=True, default='')
    source = models.CharField(max_length=100, null=True)
    is_deleted = models.BooleanField(default=False)

    def to_dic(self):
        temp_dict = dict([ (attr, getattr(self, attr)) for attr in [ f.name for f in self._meta.fields if f.name != 'app' ] ])
        temp_dict['app'] = self.app.to_dic()
        return temp_dict


class ConfigServer(models.Model):
    when_created = models.CharField(max_length=100)
    server = models.ForeignKey(Servers, null=True)
    is_delete = models.BooleanField(default=False)
    created_by = models.CharField(max_length=100, null=True)

    def to_dic(self):
        temp_dict = dict([ (attr, getattr(self, attr)) for attr in [ f.name for f in self._meta.fields if f.name != 'server' ] ])
        temp_dict['server'] = self.server.to_dic()
        return temp_dict


class ConfigInfo(models.Model):
    config_item = models.ForeignKey(ConfigItem, null=True)
    value = models.TextField(null=True)
    server_ip = models.ForeignKey(ConfigServer, null=True)
    is_delete = models.BooleanField(default=False)

    def to_dic(self):
        temp_dict = dict([ (attr, getattr(self, attr)) for attr in [ f.name for f in self._meta.fields if f.name != 'config_item' and f.name != 'server_ip' ] ])
        temp_dict['config_item'] = self.config_item.to_dic()
        temp_dict['server_ip'] = self.server_ip.to_dic()
        return temp_dict


class CustomInfo(models.Model):
    config_item = models.ForeignKey(ConfigItem)
    value = models.TextField()
    server = models.ForeignKey(Servers)

    def to_dic(self):
        return dict([ (attr, getattr(self, attr)) for attr in [ f.name for f in self._meta.fields ] ])


class CeleryTimeSet(models.Model):
    first_time = models.CharField(max_length=100)
    run_time = models.CharField(max_length=100)
    time_interval = models.IntegerField(default=0)
    time_type = models.CharField(max_length=10)
    is_deleted = models.BooleanField(default=False)

    def to_dic(self):
        return dict([ (attr, getattr(self, attr)) for attr in [ f.name for f in self._meta.fields ] ])


class CheckItem(models.Model):
    cn_name = models.CharField(max_length=100)
    os_type = models.CharField(max_length=20, default='1')
    compare_way = models.CharField(max_length=100, null=True, default=None)
    enabled_change = models.BooleanField(default=False)
    menu_name = models.CharField(max_length=100, null=True, default=None)
    name = models.CharField(max_length=100)
    item_type = models.CharField(max_length=10)
    value_type = models.CharField(max_length=10, null=True, default=None)
    severity_level = models.CharField(max_length=10, null=True, default=None)
    first_menu_name = models.CharField(max_length=100, null=True, default=None)
    is_show = models.BooleanField(default=True)
    is_selected = models.BooleanField(default=False)

    def to_dic(self):
        return dict([ (attr, getattr(self, attr)) for attr in [ f.name for f in self._meta.fields ] ])


class ReportsTemplate(models.Model):
    description = models.CharField(max_length=100, null=True, default=None)
    name = models.CharField(max_length=100)

    def to_dic(self):
        return dict([ (attr, getattr(self, attr)) for attr in [ f.name for f in self._meta.fields ] ])


class ItemTemplate(models.Model):
    item = models.ForeignKey(CheckItem)
    template = models.ForeignKey(ReportsTemplate)


class CheckModule(models.Model):
    name = models.CharField(max_length=100)
    os_type = models.CharField(max_length=20, default='1')
    when_created = models.CharField(max_length=30)
    created_by = models.CharField(max_length=100)
    modified_by = models.CharField(max_length=100, default='')
    when_modified = models.CharField(max_length=30, default='')
    base_module_id = models.IntegerField(default=0)
    is_build_in = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    description = models.TextField(default='')

    class Meta:
        verbose_name = '\xe8\x87\xaa\xe5\xae\x9a\xe4\xb9\x89\xe6\xa8\xa1\xe6\x9d\xbf'

    @property
    def get_key_items(self):
        return [{'key': '{0}.name', 'name': '\xe6\xa8\xa1\xe6\x9d\xbf\xe5\x90\x8d', 'order': 1}, {'key': '{0}.base_module_id', 'name': '\xe5\x9f\xba\xe5\x87\x86\xe6\xa8\xa1\xe6\x9d\xbf', 'order': 2}, {'key': '{0}.items', 'name': '\xe6\xa8\xa1\xe6\x9d\xbf\xe9\xa1\xb9', 'order': 3}, {'key': '{0}.description', 'name': '\xe6\x8f\x8f\xe8\xbf\xb0', 'order': 4}]

    def get_summary_title(self):
        return ('\xe8\x87\xaa\xe5\xae\x9a\xe4\xb9\x89\xe6\xa8\xa1\xe6\x9d\xbf[{0}]').format(self.name)

    def to_dic(self):
        return dict([ (attr, getattr(self, attr)) for attr in [ f.name for f in self._meta.fields ] ])

    def create_item(self, dict_item):
        self.name = dict_item['name']
        self.created_by = dict_item['created_by']
        self.base_module_id = dict_item['base_module_id']
        self.when_created = str(datetime.datetime.now()).split('.')[0]
        self.description = dict_item['description']
        self.os_type = dict_item['os_type']
        self.save()

    def modify_item(self, dict_item):
        self.name = dict_item['name']
        self.base_module_id = dict_item['base_module_id']
        self.when_modified = str(datetime.datetime.now()).split('.')[0]
        self.modified_by = dict_item['modified_by']
        self.description = dict_item['description']
        self.save()

    def get_add_operate_detail(self):
        detail = []
        item_list = self.get_key_items
        item_list.sort(lambda x, y: cmp(x['order'], y['order']))
        for i in item_list:
            if i['name'] == '\xe6\xa8\xa1\xe6\x9d\xbf\xe9\xa1\xb9':
                items = CheckItemValue.objects.filter(check_module_id=self.id).values('check_item__cn_name').distinct()
                add_items = self.format_add_items(items, 'check_item__cn_name')
                value = {'addItems': add_items, 'updateItems': [], 'deleteItems': []}
                detail.append({'name': i['name'], 'value': value, 'is_list': True})
            elif i['name'] == '\xe5\x9f\xba\xe5\x87\x86\xe6\xa8\xa1\xe6\x9d\xbf':
                value = CheckModule.objects.get(id=self.base_module_id).name
                detail.append({'name': i['name'], 'value': value, 'is_list': False})
            else:
                detail.append({'name': i['name'], 'value': eval(i['key'].format('self')), 'is_list': False})

        return detail

    def get_update_operate_detail(self, old_model):
        detail = []
        item_list = self.get_key_items
        item_list.sort(lambda x, y: cmp(x['order'], y['order']))
        for i in item_list:
            if i['name'] == '\xe6\xa8\xa1\xe6\x9d\xbf\xe9\xa1\xb9':
                add_item_list, update_item_list, delete_item_list = self.format_check_item_update(old_model)
                value = {'addItems': add_item_list, 'updateItems': update_item_list, 'deleteItems': delete_item_list}
                if len(add_item_list) + len(update_item_list) + len(delete_item_list) == 0:
                    continue
                detail.append({'name': i['name'], 'value': value, 'is_list': True})
            else:
                if i['name'] == '\xe5\x9f\xba\xe5\x87\x86\xe6\xa8\xa1\xe6\x9d\xbf':
                    new_value = CheckModule.objects.get(id=self.base_module_id).name
                    old_value = CheckModule.objects.get(id=old_model.base_module_id).name
                else:
                    new_value = eval(i['key'].format('self'))
                    old_value = eval(i['key'].format('old_model'))
                if old_value != new_value:
                    value = ('[{0}] ==> [{1}]').format(old_value, new_value)
                    detail.append({'name': i['name'], 'value': value, 'is_list': False})

        return detail

    def format_check_item_update(self, old_model):
        old_items = old_model.check_items
        old_item_id = [ x['check_item_id'] for x in old_items ]
        new_items = list(CheckItemValue.objects.filter(check_module_id=self.id).values('check_item_id', 'value'))
        new_item_id = [ x['check_item_id'] for x in new_items ]
        add_items = [ x for x in new_item_id if x not in old_item_id ]
        delete_items = [ x for x in old_item_id if x not in new_item_id ]
        add_check_items = CheckItem.objects.filter(id__in=add_items).values('cn_name').distinct()
        add_item_list = self.format_add_items(add_check_items, 'cn_name')
        delete_item_list = [ y['cn_name'] for y in CheckItem.objects.filter(id__in=delete_items).values('cn_name').distinct()
                           ]
        update_item_id = [ x for x in new_item_id if x in old_item_id ]
        update_item_list = self.format_update_items(old_items, new_items, update_item_id)
        return (add_item_list, update_item_list, delete_item_list)

    def format_add_items(self, items, key):
        add_items = []
        for x in items:
            check_item_value = CheckItemValue.objects.get(check_item__cn_name=x[key], check_module_id=self.id)
            one_obj = ('{0}\xef\xbc\x9a{1}').format(check_item_value.check_item.cn_name, check_item_value.value)
            add_items.append(one_obj)

        return add_items

    def format_update_items(self, old_items, new_items, update_item_id):
        update_items = []
        for i in update_item_id:
            old_item = [ x for x in old_items if x['check_item_id'] == i ][0]
            new_item = [ x for x in new_items if x['check_item_id'] == i ][0]
            if old_item['value'] != new_item['value']:
                check_item = CheckItem.objects.get(id=i)
                one_obj = ('{0}\xef\xbc\x9a{1} ==> {2}').format(check_item.cn_name, old_item['value'], new_item['value'])
                update_items.append(one_obj)

        return update_items


class CheckItemValue(models.Model):
    check_item = models.ForeignKey(CheckItem)
    check_module = models.ForeignKey(CheckModule)
    value = models.TextField()


class CheckTask(models.Model):
    name = models.CharField(max_length=100)
    created_by = models.CharField(max_length=100)
    ip_list = models.TextField()
    is_deleted = models.BooleanField(default=False)
    modified_by = models.CharField(max_length=100, default='')
    receivers = models.TextField()
    check_module = models.ForeignKey(CheckModule)
    script_account = models.CharField(max_length=100)
    celery_time_set = models.OneToOneField(CeleryTimeSet)
    when_created = models.CharField(max_length=100)
    when_modified = models.CharField(max_length=100, default='')
    group_list = models.TextField(default='[]')
    topo_list = models.TextField(default='[]')
    select_type = models.CharField(max_length=20, default='ip')

    class Meta:
        verbose_name = '\xe5\xb7\xa1\xe6\xa3\x80\xe4\xbb\xbb\xe5\x8a\xa1'

    @property
    def get_key_items(self):
        return [{'key': '{0}.name', 'name': '\xe4\xbb\xbb\xe5\x8a\xa1\xe5\x90\x8d', 'order': 1}, {'key': '{0}.check_module.name', 'name': '\xe9\x80\x89\xe6\x8b\xa9\xe6\xa8\xa1\xe6\x9d\xbf', 'order': 2}, {'key': '{0}.ip_list', 'name': '\xe6\x9c\x8d\xe5\x8a\xa1\xe5\x99\xa8', 'order': 3}, {'key': '{0}.group_list', 'name': '\xe5\x8a\xa8\xe6\x80\x81\xe5\x88\x86\xe7\xbb\x84', 'order': 3}, {'key': '{0}.topo_list', 'name': '\xe4\xb8\x9a\xe5\x8a\xa1\xe6\x8b\x93\xe6\x89\x91', 'order': 3}, {'key': 'time_type[{0}.celery_time_set.time_type]', 'name': '\xe4\xbb\xbb\xe5\x8a\xa1\xe7\xb1\xbb\xe5\x9e\x8b', 'order': 4}, {'key': '{0}.celery_time_set.first_time', 'name': '\xe6\x89\xa7\xe8\xa1\x8c\xe6\x97\xb6\xe9\x97\xb4', 'order': 5}, {'key': '{0}.celery_time_set.time_interval', 'name': '\xe5\x91\xa8\xe6\x9c\x9f\xe9\x97\xb4\xe9\x9a\x94', 'order': 6}, {'key': '{0}.script_account', 'name': '\xe6\x89\xa7\xe8\xa1\x8c\xe5\xb8\x90\xe5\x8f\xb7', 'order': 7}, {'key': '{0}.receivers', 'name': '\xe6\x8a\xa5\xe5\x91\x8a\xe9\x82\xae\xe7\xae\xb1', 'order': 8}]

    def to_dic(self):
        temp_dict = dict([ (attr, getattr(self, attr)) for attr in [ f.name for f in self._meta.fields if f.name != 'celery_time_set' and f.name != 'check_module' ] ])
        temp_dict['celery_time_set'] = self.celery_time_set.to_dic()
        temp_dict['check_module'] = self.check_module.to_dic()
        temp_dict['servers'] = eval(self.ip_list)
        temp_dict['groups'] = eval(self.group_list)
        temp_dict['topos'] = eval(self.topo_list)
        temp_dict['check_module_id'] = self.check_module_id
        temp_dict['type_name'] = TimeType[self.celery_time_set.time_type]
        temp_dict = dict(temp_dict, **temp_dict['celery_time_set'])
        return temp_dict

    def get_summary_title(self):
        return ('\xe5\xb7\xa1\xe6\xa3\x80\xe4\xbb\xbb\xe5\x8a\xa1[{0}]').format(self.name)

    def get_run_operate_detail(self):
        return ('\xe6\x89\xa7\xe8\xa1\x8c\xe5\xb7\xa1\xe6\xa3\x80\xe4\xbb\xbb\xe5\x8a\xa1[{0}]').format(self.name)

    def get_add_operate_detail(self):
        detail = []
        time_type = {'now': '\xe7\xab\x8b\xe5\x8d\xb3\xe6\x89\xa7\xe8\xa1\x8c', 
           'time': '\xe5\xae\x9a\xe6\x97\xb6', 
           'cycle': '\xe5\x91\xa8\xe6\x9c\x9f'}
        item_list = self.get_key_items
        item_list.sort(lambda x, y: cmp(x['order'], y['order']))
        if self.celery_time_set.time_type != 'cycle':
            item_list.pop(5)
        for i in item_list:
            if i['name'] == '\xe6\x9c\x8d\xe5\x8a\xa1\xe5\x99\xa8':
                ip_list = eval(i['key'].format('self'))
                ip_list = eval(str(ip_list))
                ip_list.sort(lambda x, y: cmp(x['ip'], y['ip']))
                value = (',').join([ x['ip'] + ('\xef\xbc\x88{0}\xef\xbc\x89').format(x['source_name']) for x in ip_list ])
                detail.append({'name': i['name'], 'value': value, 'is_list': False})
            elif i['name'] == '\xe5\x8a\xa8\xe6\x80\x81\xe5\x88\x86\xe7\xbb\x84':
                group_list = eval(i['key'].format('self'))
                group_list = eval(str(group_list))
                value = (',').join([ x['group_name'] for x in group_list ])
                detail.append({'name': i['name'], 'value': value, 'is_list': False})
            elif i['name'] == '\xe4\xb8\x9a\xe5\x8a\xa1\xe6\x8b\x93\xe6\x89\x91':
                node_list = eval(i['key'].format('self'))
                node_list = eval(str(node_list))
                value = (',').join([ x['node_name'] for x in node_list ])
                detail.append({'name': i['name'], 'value': value, 'is_list': False})
            else:
                detail.append({'name': i['name'], 'value': eval(i['key'].format('self')), 'is_list': False})

        return detail

    def get_update_operate_detail(self, old_model):
        detail = []
        time_type = {'now': '\xe7\xab\x8b\xe5\x8d\xb3\xe6\x89\xa7\xe8\xa1\x8c', 
           'time': '\xe5\xae\x9a\xe6\x97\xb6', 
           'cycle': '\xe5\x91\xa8\xe6\x9c\x9f'}
        item_list = self.get_key_items
        item_list.sort(lambda x, y: cmp(x['order'], y['order']))
        for i in item_list:
            old_value = eval(i['key'].format('old_model'))
            new_value = eval(i['key'].format('self'))
            if i['name'] == '\xe6\x89\xa7\xe8\xa1\x8c\xe6\x97\xb6\xe9\x97\xb4':
                new_value = new_value or '\xe7\xab\x8b\xe5\x8d\xb3\xe6\x89\xa7\xe8\xa1\x8c'
                old_value = old_value or '\xe7\xab\x8b\xe5\x8d\xb3\xe6\x89\xa7\xe8\xa1\x8c'
            elif i['name'] == '\xe6\x9c\x8d\xe5\x8a\xa1\xe5\x99\xa8':
                old_value = eval(old_value)
                new_value = eval(str(new_value))
                old_value.sort(lambda x, y: cmp(x['ip'], y['ip']))
                new_value.sort(lambda x, y: cmp(x['ip'], y['ip']))
                old_value = (',').join([ x['ip'] + ('\xef\xbc\x88{0}\xef\xbc\x89').format(x['source_name']) for x in old_value ])
                new_value = (',').join([ x['ip'] + ('\xef\xbc\x88{0}\xef\xbc\x89').format(x['source_name']) for x in new_value ])
            if old_value != new_value:
                detail.append({'name': i['name'], 'value': ('[{0}] ==> [{1}]').format(old_value, new_value), 'is_list': False})

        return detail


class CheckReport(models.Model):
    check_task = models.ForeignKey(CheckTask, null=True, on_delete=models.SET_NULL)
    check_task_name = models.CharField(max_length=100, default='')
    check_task_created_by = models.CharField(max_length=100, default='')
    check_module = models.ForeignKey(CheckModule, on_delete=models.PROTECT, null=True)
    when_created = models.CharField(max_length=100)
    report_info = models.CharField(max_length=200, null=True)
    status = models.CharField(max_length=100, null=True, default='RUNNING')
    total_job_num = models.IntegerField(default=1)
    finish_num = models.IntegerField(default=1)
    server_num = models.IntegerField(default=0)
    error_summary = models.TextField(default=json.dumps([]))
    total_num = models.IntegerField(default=0)

    class Meta:
        verbose_name = '\xe5\xb7\xa1\xe6\xa3\x80\xe6\x8a\xa5\xe5\x91\x8a'

    def to_dic(self):
        temp_dict = dict([ (attr, getattr(self, attr)) for attr in [ f.name for f in self._meta.fields if f.name != 'check_task' ] ])
        temp_dict['check_task'] = self.check_task.to_dic()
        return temp_dict

    def get_summary_title(self):
        return ('\xe5\xb7\xa1\xe6\xa3\x80\xe6\x8a\xa5\xe5\x91\x8a[{0}]').format(self.check_task_name)

    def get_add_operate_detail(self):
        detail = []
        return detail


class ServerReport(models.Model):
    check_report = models.ForeignKey(CheckReport)
    ip_address = models.CharField(max_length=50)
    app_id = models.IntegerField()
    app_name = models.CharField(default='', max_length=100)
    source = models.IntegerField()
    is_success = models.BooleanField(default=True)
    source_name = models.CharField(default='', max_length=100)
    summary = models.TextField(default='')

    def to_dic(self):
        temp_dict = dict([ (attr, getattr(self, attr)) for attr in [ f.name for f in self._meta.fields if f.name != 'check_report' ] ])
        temp_dict['check_report'] = self.check_report.to_dic()
        return temp_dict


class ServerReportDetail(models.Model):
    check_item = models.ForeignKey(CheckItem, default=None, null=True)
    server_report = models.ForeignKey(ServerReport)
    value = models.TextField()
    warn_status = models.BooleanField(default=False)

    def to_dic(self):
        temp_dict = dict([ (attr, getattr(self, attr)) for attr in [ f.name for f in self._meta.fields if f.name != 'check_item' and f.name != 'server_report' ] ])
        temp_dict['check_item'] = self.check_item.to_dic()
        temp_dict['server_report'] = self.server_report.to_dic()
        return temp_dict


class ReportsSubscibe(models.Model):
    name = models.CharField(max_length=100)
    created_by = models.CharField(max_length=100)
    ip_list = models.TextField()
    is_deleted = models.BooleanField(default=False)
    modified_by = models.CharField(max_length=100)
    receivers = models.TextField()
    celery_time_set = models.OneToOneField(CeleryTimeSet, null=True, default=None)
    when_created = models.CharField(max_length=100, null=True, default=None)
    when_modified = models.CharField(max_length=100, null=True, default=None)
    reports_template = models.ForeignKey(ReportsTemplate)
    when_start = models.CharField(max_length=100, null=True, default=None)
    when_end = models.CharField(max_length=100, null=True, default=None)
    time_type = models.CharField(max_length=100, null=True)
    time_interval = models.IntegerField(null=True, default=None)

    def to_dic(self):
        temp_dict = dict([ (attr, getattr(self, attr)) for attr in [ f.name for f in self._meta.fields if f.name != 'celery_time_set' and f.name != 'reports_template' ] ])
        temp_dict['celery_time_set'] = self.celery_time_set.to_dic()
        temp_dict['reports_template'] = self.reports_template.to_dic()
        return temp_dict


class SubscibeDetail(models.Model):
    check_item = models.ForeignKey(CheckItem)
    value = models.TextField()
    when_created = models.CharField(max_length=100)
    server_report = models.ForeignKey(ServerReport, null=True)
    is_warn = models.BooleanField(default=False)

    def to_dic(self):
        temp_dict = dict([ (attr, getattr(self, attr)) for attr in [ f.name for f in self._meta.fields if f.name != 'check_item' ] ])
        temp_dict['check_item'] = self.check_item.to_dic()
        return temp_dict


class MailReceiver(models.Model):
    account = models.CharField(max_length=100)
    mailbox = models.CharField(max_length=50)
    when_created = models.CharField(max_length=50)
    created_by = models.CharField(max_length=100, default='')

    def to_dic(self):
        return dict([ (attr, getattr(self, attr)) for attr in [ f.name for f in self._meta.fields ] ])

    class Meta:
        verbose_name = '\xe9\x82\xae\xe7\xae\xb1'

    @property
    def get_key_items(self):
        return [{'key': '{0}.account', 'name': '\xe5\xb8\x90\xe5\x8f\xb7', 'order': 1}, {'key': '{0}.mailbox', 'name': '\xe9\x82\xae\xe7\xae\xb1', 'order': 2}]

    def get_summary_title(self):
        return ('\xe9\x82\xae\xe7\xae\xb1[{0}]').format(self.mailbox)

    def get_add_operate_detail(self):
        detail = []
        item_list = self.get_key_items
        item_list.sort(lambda x, y: cmp(x['order'], y['order']))
        for i in item_list:
            detail.append({'name': i['name'], 'value': eval(i['key'].format('self')), 'is_list': False})

        return detail

    def get_update_operate_detail(self, old_model):
        detail = []
        item_list = self.get_key_items
        item_list.sort(lambda x, y: cmp(x['order'], y['order']))
        for i in item_list:
            new_value = eval(i['key'].format('self'))
            old_value = eval(i['key'].format('old_model'))
            if old_value != new_value:
                value = ('[{0}] ==> [{1}]').format(old_value, new_value)
                detail.append({'name': i['name'], 'value': value, 'is_list': False})

        return detail


class ScriptContent(models.Model):
    os_type = models.CharField(max_length=20, default='1')
    name = models.CharField(max_length=100)
    content = models.TextField()
    description = models.CharField(max_length=200, null=True, default=None)

    def to_dic(self):
        return dict([ (attr, getattr(self, attr)) for attr in [ f.name for f in self._meta.fields ] ])


class OperationLog(models.Model):
    operator = models.CharField(max_length=100, null=True)
    operate_type = models.TextField(max_length=100)
    operate_detail = models.TextField(default='')
    when_created = models.CharField(null=True, max_length=100)
    operate_obj = models.CharField(max_length=100, default='')
    operate_summary = models.TextField(default='')

    @property
    def OperateType(self):
        return {'add': '\xe6\x96\xb0\xe5\xa2\x9e', 'update': '\xe4\xbf\xae\xe6\x94\xb9', 'api': 'API\xe6\x89\xa7\xe8\xa1\x8c', 'delete': '\xe5\x88\xa0\xe9\x99\xa4'}

    def to_dict(self):
        dict_obj = {'operator': self.operator, 
           'when_created': self.when_created, 
           'operate_type': self.operate_type, 
           'operate_type_name': self.OperateType[self.operate_type], 
           'operate_obj': self.operate_obj, 
           'operate_summary': self.operate_summary, 
           'operate_detail': eval(self.operate_detail)}
        return dict_obj

    def create_log(self, old_model, new_model, operate_type, operator):
        self.operate_type = operate_type
        self.operator = operator
        self.when_created = str(datetime.datetime.now()).split('.')[0]
        title = new_model.get_summary_title() if new_model else old_model.get_summary_title()
        self.operate_summary = self.OperateType[operate_type] + title
        self.operate_obj = new_model._meta.verbose_name if new_model else old_model._meta.verbose_name
        if operate_type == 'add':
            self.operate_detail = new_model.get_add_operate_detail()
        elif operate_type == 'update':
            self.operate_detail = new_model.get_update_operate_detail(old_model)
        elif operate_type == 'delete':
            self.operate_detail = old_model.get_add_operate_detail()
        else:
            self.operate_detail = old_model.get_add_operate_detail()
        self.save()


class ItemMenu(models.Model):
    name = models.CharField(max_length=100)
    child_name = models.CharField(max_length=100, null=True)
    order = models.IntegerField()
    child_order = models.IntegerField()

    def to_dic(self):
        return dict([ (attr, getattr(self, attr)) for attr in [ f.name for f in self._meta.fields ] ])


class SysConfig(models.Model):
    key = models.CharField(max_length=100)
    value = models.TextField()

    def to_dic(self):
        return dict([ (attr, getattr(self, attr)) for attr in [ f.name for f in self._meta.fields ] ])


class GlobalSetting(models.Model):
    config_account = models.CharField(max_length=100, null=True)
    report_save = models.IntegerField(default=0, null=True)
    reports_save = models.CharField(max_length=100, null=True)
    created_by = models.CharField(max_length=100, null=True)

    def to_dic(self):
        return dict([ (attr, getattr(self, attr)) for attr in [ f.name for f in self._meta.fields ] ])


class CustomItem(models.Model):
    name = models.CharField(max_length=100)
    cn_name = models.CharField(max_length=100)
    description = models.TextField(default='', null=True)
    script_content = models.TextField()
    created_by = models.CharField(max_length=100)
    when_created = models.CharField(max_length=30)
    when_modified = models.CharField(max_length=30, default='')
    compare_way = models.CharField(max_length=10)
    compare_value = models.TextField()
    os_type = models.CharField(max_length=20, default='1')

    class Meta:
        verbose_name = '\xe8\x87\xaa\xe5\xae\x9a\xe4\xb9\x89\xe5\xb7\xa1\xe6\xa3\x80\xe9\xa1\xb9'

    def to_dic(self):
        return dict([ (attr, getattr(self, attr)) for attr in [ f.name for f in self._meta.fields ] ])

    def create_item(self, dict_item):
        self.name = dict_item['name']
        self.cn_name = dict_item['cn_name']
        self.description = dict_item['description']
        self.script_content = dict_item['script_content']
        self.created_by = dict_item['created_by']
        self.compare_way = dict_item['compare_way']
        self.compare_value = dict_item['compare_value']
        self.when_created = str(datetime.datetime.now()).split('.')[0]
        self.os_type = dict_item['os_type']
        self.save()

    def modify_item(self, dict_item):
        self.name = dict_item['name']
        self.cn_name = dict_item['cn_name']
        self.description = dict_item['description']
        self.script_content = dict_item['script_content']
        self.when_modified = str(datetime.datetime.now()).split('.')[0]
        self.compare_way = dict_item['compare_way']
        self.compare_value = dict_item['compare_value']
        self.save()

    @property
    def get_key_items(self):
        return [{'key': '{0}.name', 'name': '\xe5\xb7\xa1\xe6\xa3\x80\xe5\xad\x97\xe6\xae\xb5', 'order': 1}, {'key': '{0}.cn_name', 'name': '\xe5\xb7\xa1\xe6\xa3\x80\xe9\xa1\xb9\xe5\x90\x8d\xe7\xa7\xb0', 'order': 2}, {'key': '{0}.compare_way', 'name': '\xe5\xaf\xb9\xe6\xaf\x94\xe6\x96\xb9\xe5\xbc\x8f', 'order': 3}, {'key': '{0}.compare_value', 'name': '\xe5\xaf\xb9\xe6\xaf\x94\xe5\x80\xbc', 'order': 5}, {'key': '{0}.script_content', 'name': '\xe6\x89\xa7\xe8\xa1\x8c\xe8\x84\x9a\xe6\x9c\xac', 'order': 6}, {'key': '{0}.description', 'name': '\xe5\xa4\x87\xe6\xb3\xa8', 'order': 7}]

    def get_summary_title(self):
        return ('\xe8\x87\xaa\xe5\xae\x9a\xe4\xb9\x89\xe5\xb7\xa1\xe6\xa3\x80\xe9\xa1\xb9[{0}]').format(self.cn_name)

    def get_add_operate_detail(self):
        detail = []
        item_list = self.get_key_items
        item_list.sort(lambda x, y: cmp(x['order'], y['order']))
        for i in item_list:
            detail.append({'name': i['name'], 'value': eval(i['key'].format('self')), 'is_list': False})

        return detail

    def get_update_operate_detail(self, old_model):
        detail = []
        item_list = self.get_key_items
        item_list.sort(lambda x, y: cmp(x['order'], y['order']))
        for i in item_list:
            new_value = eval(i['key'].format('self'))
            old_value = eval(i['key'].format('old_model'))
            if old_value != new_value:
                value = ('[{0}] ==> [{1}]').format(old_value, new_value)
                detail.append({'name': i['name'], 'value': value, 'is_list': False})

        return detail


class CustomItemValue(models.Model):
    custom_item = models.ForeignKey(CustomItem)
    check_module = models.ForeignKey(CheckModule)
    value = models.TextField()


class CustomReportDetail(models.Model):
    custom_item = models.ForeignKey(CustomItem)
    server_report = models.ForeignKey(ServerReport)
    value = models.TextField()
    is_warn = models.BooleanField(default=False)

    def to_dic(self):
        temp_dict = dict([ (attr, getattr(self, attr)) for attr in [ f.name for f in self._meta.fields if f.name != 'custom_item' and f.name != 'server_report' ] ])
        temp_dict['custom_item'] = self.custom_item.to_dic()
        temp_dict['server_report'] = self.server_report.to_dic()
        return temp_dict


class LogoImg(models.Model):
    key = models.CharField(max_length=100)
    value = models.BinaryField()