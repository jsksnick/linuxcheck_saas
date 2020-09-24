# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.9 Stackless 3.1b3 060516 (default, Nov 28 2016, 09:05:13) 
# [GCC 4.4.7 20120313 (Red Hat 4.4.7-17)]
# Embedded file name: /bkdata/vcs2/tmp/linuxcheck_saas-1561098846.95/linuxcheck_saas/src/home_application/module_view.py
# Compiled at: 2019-06-21 14:34:36
from common.mymako import render_json
from common.log import logger
from home_application.models import *
import json
from django.db.models import Q

def search_module_list(request):
    try:
        filter_obj = eval(request.body)
        if not filter_obj['os_type']:
            module_list = CheckModule.objects.filter(name__icontains=filter_obj['name'], is_deleted=False)
        else:
            module_list = CheckModule.objects.filter(name__icontains=filter_obj['name'], os_type=filter_obj['os_type'], is_deleted=False)
        if not request.user.is_superuser:
            module_list = module_list.filter(created_by=request.user.username)
        return_data = list(module_list.values())
        for i in return_data:
            i['os_type_name'] = 'SUSE' if i['os_type'] == '2' else 'CentOS\\Redhat'

        return render_json({'result': True, 'data': return_data})
    except Exception as e:
        logger.exception(e)
        return render_json({'result': False, 'data': [u'\u7cfb\u7edf\u5f02\u5e38\uff0c\u8bf7\u8054\u7cfb\u7ba1\u7406\u5458\uff01']})


def get_module_list(request):
    try:
        filter_obj = eval(request.body)
        if not filter_obj['type_id']:
            render_json({'result': False, 'data': [u'\u8bf7\u9009\u62e9\u7cfb\u7edf\u7c7b\u578b']})
        module_list = CheckModule.objects.filter(is_deleted=False, os_type=str(filter_obj['type_id']))
        if not request.user.is_superuser:
            module_list = module_list.filter(Q(created_by=request.user.username) | Q(created_by='system'))
        return render_json({'result': True, 'data': [ {'id': i.id, 'text': i.name + '(' + i.created_by + ')'} for i in module_list ]})
    except Exception as e:
        logger.exception(e)
        return render_json({'result': False, 'data': [u'\u7cfb\u7edf\u5f02\u5e38\uff0c\u8bf7\u8054\u7cfb\u7ba1\u7406\u5458\uff01']})


def get_module_item_list(request):
    try:
        module_id = request.GET['module_id']
        os_type = CheckModule.objects.get(id=int(module_id)).os_type
        sys_module_id = CheckModule.objects.get(created_by='system', base_module_id=0, os_type=os_type).id
        value_list = CheckItemValue.objects.filter(check_module_id=module_id).exclude(check_item__item_type='info')
        return_data = []
        id_list = []
        for i in value_list:
            tmp = {'menu_one': i.check_item.first_menu_name, 'menu_two': i.check_item.menu_name, 'name': i.check_item.name, 
               'cn_name': i.check_item.cn_name, 'value': i.value, 'compare_way': i.check_item.compare_way, 'can_modified': i.check_item.enabled_change, 
               'is_checked': True, 'check_item_id': i.check_item.id}
            id_list.append(i.check_item_id)
            return_data.append(tmp)

        custom_item_list = get_custom_item_list(module_id)
        no_check_item_list = CheckItemValue.objects.filter(check_module_id=sys_module_id).exclude(check_item_id__in=id_list).exclude(check_item__item_type='info')
        return_data += [ {'menu_one': i.check_item.first_menu_name, 'menu_two': i.check_item.menu_name, 'name': i.check_item.name, 'cn_name': i.check_item.cn_name, 'value': i.value, 'compare_way': i.check_item.compare_way, 'can_modified': i.check_item.enabled_change, 'is_checked': False, 'check_item_id': i.check_item.id} for i in no_check_item_list
                       ]
        return_data.sort(lambda x, y: cmp(x['check_item_id'], y['check_item_id']))
        menus = ItemMenu.objects.all().values('name').order_by('order').distinct()
        menu_list = []
        for i in menus:
            menu_two = ItemMenu.objects.filter(name=i['name']).order_by('child_order')
            menu_two_list = [ {'name': u.child_name, 'isShow': True, 'is_checked': True} for u in menu_two ]
            menu_list.append({'menu_one': i['name'], 'isShow': True, 'is_checked': True, 'menu_two': menu_two_list})

        return render_json({'result': True, 'data': return_data, 'menu_list': menu_list, 'custom_item_list': custom_item_list})
    except Exception as e:
        logger.exception(e)
        return render_json({'result': False, 'data': [u'\u7cfb\u7edf\u5f02\u5e38\uff0c\u8bf7\u8054\u7cfb\u7ba1\u7406\u5458\uff01']})


def get_custom_item_list(module_id):
    custom_item_list = CustomItemValue.objects.filter(check_module_id=module_id)
    os_type = CheckModule.objects.get(id=int(module_id)).os_type
    sys_module_id = CheckModule.objects.get(created_by='system', base_module_id=0, os_type=os_type).id
    tmp = [ {'name': i.custom_item.name, 'cn_name': i.custom_item.cn_name, 'value': i.value, 'compare_way': i.custom_item.compare_way, 'can_modified': True, 'is_checked': True, 'custom_item_id': i.custom_item.id} for i in custom_item_list
          ]
    no_check_custom_item_list = CustomItemValue.objects.filter(check_module_id=sys_module_id).exclude(custom_item_id__in=[ i.custom_item_id for i in custom_item_list ])
    tmp += [ {'name': i.custom_item.name, 'cn_name': i.custom_item.cn_name, 'value': i.value, 'compare_way': i.custom_item.compare_way, 'can_modified': True, 'is_checked': False, 'custom_item_id': i.custom_item.id} for i in no_check_custom_item_list
           ]
    tmp.sort(lambda x, y: cmp(x['custom_item_id'], y['custom_item_id']))
    return tmp


def create_module(request):
    try:
        module_obj = json.loads(request.body)
        is_exist = CheckModule.objects.filter(is_deleted=False, name=module_obj['name'], created_by=request.user.username).exists()
        if is_exist:
            return render_json({'result': False, 'data': [u'\u8be5\u6a21\u677f\u540d\u79f0\u5df2\u5b58\u5728!']})
        check_module = CheckModule()
        check_module.create_item(module_obj)
        item_value_list = create_check_item_value(module_obj, check_module)
        CheckItemValue.objects.bulk_create(item_value_list)
        custom_item_value = create_custom_item_value(module_obj, check_module)
        CustomItemValue.objects.bulk_create(custom_item_value)
        log = OperationLog()
        log.create_log(None, check_module, 'add', request.user.username)
        return render_json({'result': True})
    except Exception as e:
        logger.exception(e)
        return render_json({'result': False, 'data': [u'\u7cfb\u7edf\u5f02\u5e38\uff0c\u8bf7\u8054\u7cfb\u7ba1\u7406\u5458\uff01']})

    return


def modify_module(request):
    try:
        module_obj = json.loads(request.body)
        is_exist = CheckModule.objects.filter(is_deleted=False, name=module_obj['name'], created_by=request.user.username).exclude(id=module_obj['id']).exists()
        if is_exist:
            return render_json({'result': False, 'data': [u'\u8be5\u6a21\u677f\u540d\u79f0\u5df2\u5b58\u5728!']})
        check_module = CheckModule.objects.get(id=module_obj['id'])
        old_model = CheckModule.objects.get(id=module_obj['id'])
        setattr(old_model, 'check_items', list(old_model.checkitemvalue_set.values('check_item_id', 'value')))
        check_module.modify_item(module_obj)
        CheckItemValue.objects.filter(check_module_id=module_obj['id']).delete()
        item_value_list = create_check_item_value(module_obj, check_module)
        CheckItemValue.objects.bulk_create(item_value_list)
        CustomItemValue.objects.filter(check_module_id=module_obj['id']).delete()
        custom_item_value = create_custom_item_value(module_obj, check_module)
        CustomItemValue.objects.bulk_create(custom_item_value)
        log = OperationLog()
        log.create_log(old_model, check_module, 'update', request.user.username)
        return render_json({'result': True})
    except Exception as e:
        logger.exception(e)
        return render_json({'result': False, 'data': [u'\u7cfb\u7edf\u5f02\u5e38\uff0c\u8bf7\u8054\u7cfb\u7ba1\u7406\u5458\uff01']})


def create_custom_item_value(module_obj, check_module):
    return_data = []
    for i in module_obj['custom_item_list']:
        if not i['is_checked']:
            continue
        return_data.append(CustomItemValue(custom_item_id=i['custom_item_id'], check_module_id=check_module.id, value=i['value']))

    return return_data


def create_check_item_value(module_obj, check_module):
    item_value_list = []
    for i in module_obj['check_item_list']:
        if not i['is_checked']:
            continue
        item_value_list.append(CheckItemValue(check_item_id=i['check_item_id'], check_module_id=check_module.id, value=i['value']))

    return item_value_list


def delete_module(request):
    try:
        module_obj = json.loads(request.body)
        check_tasks = CheckTask.objects.filter(check_module_id=module_obj['id'], is_deleted=False)
        if check_tasks.exists():
            err_list = [
             u'\u5220\u9664\u6a21\u677f\u524d\uff0c\u8bf7\u5148\u5220\u9664\u4f7f\u7528\u8be5\u6a21\u677f\u7684\u4efb\u52a1\uff0c\u4efb\u52a1\u540d\u79f0\u5982\u4e0b:']
            for check_task in check_tasks:
                err_list.append(check_task.name)

            return render_json({'result': False, 'data': err_list})
        CheckModule.objects.filter(id=module_obj['id']).update(is_deleted=True)
        log = OperationLog()
        check_module = CheckModule.objects.get(id=module_obj['id'])
        log.create_log(check_module, None, 'delete', request.user.username)
        return render_json({'result': True})
    except Exception as e:
        logger.exception(e)
        return render_json({'result': False, 'data': [u'\u7cfb\u7edf\u5f02\u5e38\uff0c\u8bf7\u8054\u7cfb\u7ba1\u7406\u5458\uff01']})

    return