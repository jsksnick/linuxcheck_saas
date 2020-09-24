# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.9 Stackless 3.1b3 060516 (default, Nov 28 2016, 09:05:13) 
# [GCC 4.4.7 20120313 (Red Hat 4.4.7-17)]
# Embedded file name: /bkdata/vcs2/tmp/linuxcheck_saas-1561098846.95/linuxcheck_saas/src/home_application/custom_item_view.py
# Compiled at: 2019-06-21 14:34:36
from common.mymako import render_json
from common.log import logger
from home_application.models import *
import json

def get_item_list(request):
    try:
        filter_obj = eval(request.body)
        if not filter_obj['os_type']:
            custom_items = CustomItem.objects.filter(cn_name__icontains=filter_obj['name']).order_by('-id').values()
        else:
            custom_items = CustomItem.objects.filter(cn_name__icontains=filter_obj['name'], os_type=str(filter_obj['os_type'])).order_by('-id').values()
        return_data = list(custom_items)
        for item_obj in return_data:
            item_obj['os_name'] = 'SUSE' if str(item_obj['os_type']) == '2' else 'CentOS\xe3\x80\x81Redhat'

        return render_json({'result': True, 'data': return_data})
    except Exception as e:
        logger.exception(e)
        return render_json({'result': False, 'data': [u'\u7cfb\u7edf\u5f02\u5e38\uff0c\u8bf7\u8054\u7cfb\u7ba1\u7406\u5458\uff01']})


def create_custom_item(request):
    try:
        custom_item = eval(request.body)
        is_exist = CustomItem.objects.filter(name=custom_item['name'], os_type=str(custom_item['os_type'])).exists()
        if is_exist:
            return render_json({'result': False, 'data': u'\u5de1\u68c0\u5b57\u6bb5\u540d\u5df2\u5b58\u5728\uff01'})
        is_exist = CustomItem.objects.filter(cn_name=custom_item['cn_name'], os_type=str(custom_item['os_type'])).exists()
        if is_exist:
            return render_json({'result': False, 'data': u'\u5de1\u68c0\u540d\u79f0\u5df2\u5b58\u5728\uff01'})
        item = CustomItem()
        item.create_item(custom_item)
        log = OperationLog()
        log.create_log(None, item, 'add', request.user.username)
        check_module_obj = CheckModule.objects.get(created_by='system', base_module_id=0, os_type=str(custom_item['os_type']))
        CustomItemValue.objects.create(check_module_id=check_module_obj.id, custom_item_id=item.id, value=item.compare_value)
        return render_json({'result': True})
    except Exception as e:
        logger.exception(e)
        return render_json({'result': False, 'data': [u'\u7cfb\u7edf\u5f02\u5e38\uff0c\u8bf7\u8054\u7cfb\u7ba1\u7406\u5458\uff01']})

    return


def delete_custom_item(request):
    try:
        custom_item = json.loads(request.body)
        custom_item = CustomItem.objects.get(id=custom_item['id'])
        log = OperationLog()
        log.create_log(custom_item, None, 'delete', request.user.username)
        custom_item.delete()
        return render_json({'result': True})
    except Exception as e:
        logger.exception(e)
        return render_json({'result': False, 'data': [u'\u7cfb\u7edf\u5f02\u5e38\uff0c\u8bf7\u8054\u7cfb\u7ba1\u7406\u5458\uff01']})

    return


def modify_custom_item(request):
    try:
        filter_obj = eval(request.body)
        now_time = str(datetime.datetime.now()).split('.')[0]
        is_exist = CustomItem.objects.filter(name=filter_obj['name'], os_type=str(filter_obj['os_type'])).exclude(id=int(filter_obj['id'])).exists()
        if is_exist:
            return render_json({'result': False, 'data': u'\u5de1\u68c0\u5b57\u6bb5\u5df2\u5b58\u5728\uff01'})
        is_exist = CustomItem.objects.filter(cn_name=filter_obj['cn_name'], os_type=str(filter_obj['os_type'])).exclude(id=int(filter_obj['id'])).exists()
        if is_exist:
            return render_json({'result': False, 'data': u'\u5de1\u68c0\u9879\u540d\u79f0\u5df2\u5b58\u5728\uff01'})
        old_obj = CustomItem.objects.get(id=filter_obj['id'])
        CustomItem.objects.filter(id=filter_obj['id']).update(name=filter_obj['name'], cn_name=filter_obj['cn_name'], description=filter_obj['description'], script_content=filter_obj['script_content'], when_modified=now_time, compare_way=filter_obj['compare_way'], compare_value=filter_obj['compare_value'])
        CustomItemValue.objects.filter(custom_item=old_obj).update(value=filter_obj['compare_value'])
        new_obj = CustomItem.objects.get(id=filter_obj['id'])
        log = OperationLog()
        log.create_log(old_obj, new_obj, 'update', request.user.username)
        return render_json({'result': True})
    except Exception as e:
        logger.exception(e)
        return render_json({'result': False, 'data': [u'\u7cfb\u7edf\u5f02\u5e38\uff0c\u8bf7\u8054\u7cfb\u7ba1\u7406\u5458\uff01']})