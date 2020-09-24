# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.9 Stackless 3.1b3 060516 (default, Nov 28 2016, 09:05:13) 
# [GCC 4.4.7 20120313 (Red Hat 4.4.7-17)]
# Embedded file name: /bkdata/vcs2/tmp/linuxcheck_saas-1561098846.95/linuxcheck_saas/src/home_application/task_view.py
# Compiled at: 2019-06-21 14:34:36
from account.decorators import login_exempt
from django.views.decorators.csrf import csrf_exempt
from common.mymako import render_json
from home_application.celery_tasks import *
from django.db.models import Q

def get_task_option(request):
    try:
        filter_obj = eval(request.body)
        if not filter_obj['type_id']:
            return render_json({'result': False, 'data': [u'\u8bf7\u5148\u9009\u62e9\u7cfb\u7edf\u7c7b\u578b\uff01']})
        mail_data = MailReceiver.objects.all()
        module_list = CheckModule.objects.filter(is_deleted=False, os_type=str(filter_obj['type_id']))
        if not request.user.is_superuser:
            mail_data = MailReceiver.objects.filter(created_by=request.user.username)
            module_list = module_list.filter(Q(created_by=request.user.username) | Q(created_by='system'))
        mails = [ {'text': o['mailbox'], 'id': o['mailbox']} for o in mail_data.values('mailbox').distinct() ]
        module_list_return = [ {'id': i.id, 'text': i.name + '(' + i.created_by + ')'} for i in module_list ]
        return render_json({'result': True, 'mail_list': mails, 'module_list': module_list_return})
    except Exception as e:
        logger.exception(e)
        return render_json({'result': False, 'data': [u'\u7cfb\u7edf\u5f02\u5e38\uff0c\u8bf7\u8054\u7cfb\u7ba1\u7406\u5458\uff01']})


def get_user_mail(request):
    try:
        mail_data = MailReceiver.objects.all()
        if not request.user.is_superuser:
            mail_data = MailReceiver.objects.filter(created_by=request.user.username)
        mails = [ {'text': o['mailbox'], 'id': o['mailbox']} for o in mail_data.values('mailbox').distinct() ]
        return render_json({'result': True, 'data': mails})
    except Exception as e:
        logger.exception(e)
        return render_json({'result': False})


def create_task(request):
    try:
        task_obj = json.loads(request.body)
        task_exist = CheckTask.objects.filter(name=task_obj['name'], created_by=request.user.username, is_deleted=False).exists()
        if task_exist:
            return render_json({'result': False, 'data': [u'\u8be5\u4efb\u52a1\u540d\u79f0\u5df2\u5b58\u5728\uff01']})
        time_set = create_time_set(task_obj)
        check_task = CheckTask.objects.create(name=task_obj['name'], created_by=request.user.username, when_created=str(datetime.datetime.now()).split('.')[0], ip_list=task_obj['servers'], receivers=task_obj['receivers'], celery_time_set_id=time_set.id, script_account=task_obj['script_account'], check_module_id=task_obj['check_module_id'], group_list=task_obj['groups'], topo_list=task_obj['nodes'], select_type=task_obj['select_type'])
        if task_obj['time_type'] == 'now':
            run_task.delay(time_set.id)
        else:
            start_time = time_set.first_time
            run_time = datetime.datetime.strptime(start_time, '%Y-%m-%d %H:%M')
            run_task.apply_async(args=[time_set.id], eta=run_time)
        log = OperationLog()
        log.create_log(None, check_task, 'add', request.user.username)
        return render_json({'result': True})
    except Exception as e:
        logger.exception(e)
        return render_json({'result': False, 'data': [u'\u7cfb\u7edf\u5f02\u5e38\uff0c\u8bf7\u8054\u7cfb\u7ba1\u7406\u5458\uff01']})

    return


@csrf_exempt
@login_exempt
def create_check_job_by_api(request):
    """\xe5\xba\x94\xe7\x94\xa8\xe5\xb7\xa1\xe6\xa3\x80app\xe8\xb0\x83\xe7\x94\xa8\xe6\x8e\xa5\xe5\x8f\xa3"""
    try:
        task_id = json.loads(request.body).get('task_id', '')
        if not task_id:
            return render_json({'result': False, 'data': u'\u6ca1\u6709\u4efb\u52a1id'})
        task_obj = CheckTask.objects.get(id=task_id)
        run_task.delay(task_obj.celery_time_set_id, False)
        log = OperationLog()
        log.create_log(task_obj, None, 'api', request.user.username)
        time.sleep(5)
        report_obj = CheckReport.objects.filter(check_task_id=task_id).last()
        return render_json({'result': True, 'data': report_obj.id})
    except Exception as e:
        logger.exception(e)
        return render_json({'result': False, 'data': e.message})

    return


def create_time_set(task_obj):
    gap = 0
    if task_obj['time_type'] == 'now':
        first_time = '\xe7\xab\x8b\xe5\x8d\xb3'
        next_time = ''
    elif task_obj['time_type'] == 'time':
        first_time = task_obj['runTime']
        next_time = task_obj['runTime']
    else:
        first_time = task_obj['cycleTime']
        next_time = task_obj['cycleTime']
        gap = task_obj['interval']
    time_set = CeleryTimeSet.objects.create(first_time=first_time, run_time=next_time, time_interval=gap, time_type=task_obj['time_type'])
    return time_set


def get_task_list(request):
    try:
        filter_obj = json.loads(request.body)
        if filter_obj['task_type'] == '00':
            filter_obj['task_type'] = ''
        task_list = CheckTask.objects.filter(is_deleted=False, name__icontains=filter_obj['task_name'], celery_time_set__time_type__icontains=filter_obj['task_type']).order_by('-when_created')
        if not request.user.is_superuser:
            task_list = task_list.filter(created_by=request.user.username)
        return_data = [ i.to_dic() for i in task_list ]
        return render_json({'result': True, 'data': return_data})
    except Exception as e:
        logger.exception(e)
        return render_json({'result': False, 'data': [u'\u7cfb\u7edf\u5f02\u5e38\uff0c\u8bf7\u8054\u7cfb\u7ba1\u7406\u5458\uff01']})


@csrf_exempt
@login_exempt
def get_check_task_by_api(request):
    try:
        task_list = CheckTask.objects.filter(is_deleted=False, celery_time_set__time_type__icontains='now')
        return_data = []
        for i in task_list.order_by('-when_created')[0:5]:
            one_obj = dict()
            one_obj['name'] = i.name
            one_obj['created_by'] = i.created_by
            one_obj['id'] = i.id
            return_data.append(one_obj)

        return render_json({'result': True, 'data': return_data})
    except Exception as e:
        logger.exception(e)
        return render_json({'result': False, 'data': e.message})


def run_task_now(request):
    try:
        task_id = request.GET['task_id']
        task_obj = CheckTask.objects.get(id=task_id)
        run_task.delay(task_obj.celery_time_set_id, False)
        log = OperationLog()
        log.create_log(task_obj, None, 'api', request.user.username)
        return render_json({'result': True})
    except Exception as e:
        logger.exception(e)
        return render_json({'result': False, 'data': u'\u7cfb\u7edf\u5f02\u5e38\uff0c\u8bf7\u8054\u7cfb\u7ba1\u7406\u5458\uff01'})

    return


def delete_task(request):
    try:
        task_obj = json.loads(request.body)
        CheckTask.objects.filter(id=task_obj['id']).update(is_deleted=True)
        CeleryTimeSet.objects.filter(checktask__id=task_obj['id']).update(is_deleted=True)
        check_task = CheckTask.objects.get(id=task_obj['id'])
        log = OperationLog()
        log.create_log(check_task, None, 'delete', request.user.username)
        return render_json({'result': True})
    except Exception as e:
        logger.exception(e)
        return render_json({'result': False, 'data': u'\u7cfb\u7edf\u5f02\u5e38\uff0c\u8bf7\u8054\u7cfb\u7ba1\u7406\u5458\uff01'})

    return


def modify_task(request):
    try:
        task_obj = json.loads(request.body)
        task_exist = CheckTask.objects.filter(name=task_obj['name'], created_by=request.user.username).exclude(id=task_obj['id']).exists()
        if task_exist:
            return render_json({'result': False, 'data': [u'\u8be5\u4efb\u52a1\u540d\u79f0\u5df2\u5b58\u5728\uff01']})
        old_task = CheckTask.objects.get(id=task_obj['id'])
        old_model = CheckTask.objects.get(id=task_obj['id'])
        old_task.celery_time_set.is_deleted = True
        old_task.celery_time_set.save()
        time_set = create_time_set(task_obj)
        CheckTask.objects.filter(id=task_obj['id']).update(name=task_obj['name'], ip_list=str(task_obj['servers']), receivers=task_obj['receivers'], celery_time_set_id=time_set.id, script_account=task_obj['script_account'], check_module_id=task_obj['check_module_id'])
        new_task = CheckTask.objects.get(id=task_obj['id'])
        if task_obj['time_type'] == 'now':
            run_task.delay(time_set.id)
        else:
            start_time = time_set.first_time
            run_time = datetime.datetime.strptime(start_time, '%Y-%m-%d %H:%M')
            run_task.apply_async(args=[time_set.id], eta=run_time)
        log = OperationLog()
        log.create_log(old_model, new_task, 'update', request.user.username)
        return render_json({'result': True})
    except Exception as e:
        logger.exception(e)
        return render_json({'result': False, 'data': [u'\u7cfb\u7edf\u5f02\u5e38\uff0c\u8bf7\u8054\u7cfb\u7ba1\u7406\u5458\uff01']})


def task_clone(request):
    """\xe4\xbb\xbb\xe5\x8a\xa1\xe5\x85\x8b\xe9\x9a\x86"""
    try:
        task_obj = json.loads(request.body)
        task_exist = CheckTask.objects.filter(name=task_obj['name'], created_by=request.user.username, is_deleted=False).exclude(id=task_obj['id']).exists()
        if task_exist:
            return render_json({'result': False, 'data': [u'\u8be5\u4efb\u52a1\u540d\u79f0\u5df2\u5b58\u5728\uff01']})
        old_task = CheckTask.objects.get(pk=task_obj['id'])
        time_set = create_time_set(task_obj)
        new_task = CheckTask.objects.create(name=task_obj['name'], created_by=request.user.username, ip_list=str(task_obj['servers']), receivers=task_obj['receivers'], script_account=task_obj['script_account'], when_created=str(datetime.datetime.now()).split('.')[0], celery_time_set_id=time_set.id, check_module_id=task_obj['check_module_id'], select_type=task_obj['select_type'], group_list=task_obj['groups'], topo_list=task_obj['nodes'])
        if task_obj['time_type'] == 'now':
            run_task.delay(time_set.id)
        else:
            start_time = time_set.first_time
            run_time = datetime.datetime.strptime(start_time, '%Y-%m-%d %H:%M')
            run_task.apply_async(args=[time_set.id], eta=run_time)
        log = OperationLog()
        log.create_log(old_task, new_task, 'add', request.user.username)
        return render_json({'result': True})
    except Exception as e:
        logger.exception(e)
        return render_json({'result': False, 'data': [u'\u7cfb\u7edf\u5f02\u5e38\uff0c\u8bf7\u8054\u7cfb\u7ba1\u7406\u5458\uff01']})


def search_dynamic_group_list(request):
    try:
        username = request.user.username
        bus_res = get_business_by_user(username)
        if not bus_res['result']:
            logger.exception(bus_res['data'])
            return render_json(bus_res)
        bus_list = [ {'app_id': i['bk_biz_id'], 'app_name': i['bk_biz_name']} for i in bus_res['data'] ]
        group_data = get_dynamic_group(username, bus_list)
        return render_json({'result': True, 'data': group_data})
    except Exception as e:
        logger.exception(e)
        return render_json({'result': False, 'data': [u'\u7cfb\u7edf\u5f02\u5e38\uff0c\u8bf7\u8054\u7cfb\u7ba1\u7406\u5458\uff01']})


def check_app_topo(request):
    try:
        tree_node = json.loads(request.body)
        username = request.user.username
        data = []
        topo_result = get_business_topo(tree_node['bk_biz_id'], tree_node['bk_biz_name'], username)
        if not topo_result['result']:
            logger.exception(topo_result['data'])
            return render_json([])
        if topo_result['data'] and topo_result['data'][0].get('child', []):
            data = topo_result['data'][0]['child']
        tree_node['child'] = data
        return_data = get_app_topo_children(tree_node, username)
        return render_json({'result': True, 'data': return_data})
    except Exception as e:
        logger.exception(e)
        return render_json({'result': False, 'data': []})


def get_app_topo_children(obj, username):
    return_data = []
    if 'child' not in obj:
        return []
    for i in obj['child']:
        one_obj = i
        one_obj['checked'] = True
        one_obj['open'] = True
        one_obj['is_open_all'] = True
        if one_obj['bk_obj_name'] != 'module':
            one_obj['child'] = get_app_topo_children(i, username)
        else:
            one_obj['isParent'] = False
        return_data.append(one_obj)

    return return_data


def get_check_topo(request):
    try:
        obj = json.loads(request.body)
        return_data = get_app_topo_children(obj, request.user.username)
        return render_json({'result': True, 'data': return_data})
    except Exception as e:
        logger.exception(e)
        return render_json({'result': False, 'data': []})


def search_app_topo(request):
    try:
        topo_type = request.GET['topo_type']
        username = request.user.username
        biz_id = request.GET['bk_biz_id']
        checked = request.GET['checked']
        check_status = True if checked == 'true' else False
        if topo_type == '1':
            topo_result = get_business_topo(biz_id, username, topo_type=False, check_status=check_status)
            if not topo_result['result']:
                logger.exception(topo_result['data'])
                return render_json([])
            if topo_result['data'] and topo_result['data'][0].get('child', []):
                return render_json(topo_result['data'][0]['child'])
            return render_json([])
    except Exception as e:
        logger.exception(e)
        return render_json({'result': False, 'data': [u'\u7cfb\u7edf\u51fa\u9519\uff0c\u8bf7\u8054\u7cfb\u7ba1\u7406\u5458']})