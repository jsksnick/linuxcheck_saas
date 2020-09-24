# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.9 Stackless 3.1b3 060516 (default, Nov 28 2016, 09:05:13) 
# [GCC 4.4.7 20120313 (Red Hat 4.4.7-17)]
# Embedded file name: /bkdata/vcs2/tmp/linuxcheck_saas-1561098846.95/linuxcheck_saas/src/home_application/sys_view.py
# Compiled at: 2019-06-21 14:34:36
import json
from home_application.celery_tasks import *
from common.mymako import render_json
from conf.default import IMG_FILE
from django.http import HttpResponse
ERROR_MSG = {'result': False, 
   'data': [
          u'\u7cfb\u7edf\u5f02\u5e38\uff0c\u8bf7\u8054\u7cfb\u7ba1\u7406\u5458\uff01']}

def search_log(request):
    filter_obj = json.loads(request.body)
    filter_obj['operateType'] = filter_obj['operateType'] if filter_obj['operateType'] != '00' else ''
    logs = OperationLog.objects.filter(when_created__range=(
     str(filter_obj['whenStart']) + ' 00:00:00', str(filter_obj['whenEnd']) + ' 23:59:59'), operate_type__icontains=filter_obj['operateType'], operator__icontains=filter_obj['operator']).order_by('-id')
    return render_json({'result': True, 'data': [ i.to_dict() for i in logs ]})


def search_mail(request):
    args = eval(request.body)
    try:
        result = MailReceiver.objects.filter(account__icontains=args['username'], mailbox__icontains=args['mailbox'])
        if not request.user.is_superuser:
            result = result.filter(created_by=request.user.username)
        return_data = [ i.to_dic() for i in result.order_by('-when_created') ]
        return render_json({'result': True, 'data': return_data})
    except Exception as e:
        logger.exception(e)
        return render_json({'result': False, 'data': [u'\u7cfb\u7edf\u5f02\u5e38\uff0c\u8bf7\u8054\u7cfb\u7ba1\u7406\u5458']})


def get_all_mail(request):
    url = ('{0}/api/c/compapi/v2/bk_login/get_all_users/').format(BK_PAAS_HOST)
    headers = {'Accept': 'application/json'}
    params = {'bk_app_code': APP_ID, 
       'bk_app_secret': APP_TOKEN, 
       'bk_username': request.user.username}
    res = requests.get(url, params=params, headers=headers, verify=False)
    result = json.loads(res.content)
    mail_list = []
    for i, j in enumerate(result['data']):
        if not result['data'][i]['email']:
            del result['data'][i]

    for i in result['data']:
        mail_list.append({'user_name': i['bk_username'], 'email': i['email']})

    return render_json({'result': True, 'data': mail_list})


def add_mail(request):
    args = eval(request.body)
    arr = []
    try:
        now = str(datetime.datetime.now()).split('.')[0]
        for i in args:
            mail_obj, is_add = MailReceiver.objects.get_or_create(account=i['user_name'], created_by=request.user.username, defaults={'when_created': now, 
               'mailbox': i['email']})
            if is_add:
                log = OperationLog()
                log.create_log(None, mail_obj, 'add', request.user.username)
                del log
                arr.append(mail_obj.to_dic())

        return render_json({'result': True, 'data': arr})
    except Exception as e:
        logger.exception(e)
        return render_json(ERROR_MSG)

    return


def delete_mail(request):
    mail_id = request.GET['id']
    try:
        mail_delete = MailReceiver.objects.get(id=mail_id)
        log = OperationLog()
        log.create_log(mail_delete, None, 'delete', request.user.username)
        mail_delete.delete()
        return render_json({'result': True})
    except Exception as e:
        logger.exception(e)
        return render_json({'result': False, 'data': [u'\u7cfb\u7edf\u5f02\u5e38\uff0c\u8bf7\u8054\u7cfb\u7ba1\u7406\u5458']})

    return


def get_count_obj(request):
    try:
        server_report = ServerReport.objects.all()
        check_report = CheckReport.objects.filter(status='COMPLETE')
        if not request.user.is_superuser:
            server_report = server_report.filter(check_report__check_task_created_by=request.user.username)
            check_report = check_report.filter(check_task_created_by=request.user.username)
        app_count = server_report.values('app_id').distinct().count()
        server_count = server_report.values('ip_address', 'source').distinct().count()
        check_count = check_report.count()
        error_count = server_report.filter(serverreportdetail__warn_status=True).values('ip_address', 'source').distinct().count()
        task_list = get_task_list_chart(request.user.username, request.user.is_superuser)
        report_list = get_report_info_list(request.user.username, request.user.is_superuser)
        return render_json({'result': True, 'data': {'app_count': app_count, 'server_count': server_count, 'check_count': check_count, 'error_count': error_count}, 
           'task_list': task_list, 
           'report_list': report_list})
    except Exception as e:
        logger.exception(e)
        return render_json({'result': False, 'data': [u'\u7cfb\u7edf\u5f02\u5e38\uff0c\u8bf7\u8054\u7cfb\u7ba1\u7406\u5458']})


def get_report_info_list(username, is_superuser):
    report_list = CheckReport.objects.filter(status='COMPLETE').exclude(serverreport=None)
    if not is_superuser:
        report_list = report_list.filter(check_task_created_by=username)
    return_data = []
    for i in report_list.order_by('-id')[:5]:
        detail_count = ServerReport.objects.filter(check_report_id=i.id).count()
        if detail_count:
            return_data.append({'id': i.id, 'text': i.when_created + ' \xe5\xae\x8c\xe6\x88\x90\xe4\xba\x86\xe4\xb8\x80\xe6\xac\xa1\xe5\xb7\xa1\xe6\xa3\x80'})

    return return_data


def get_server_error_count():
    servers = Servers.objects.exclude(operation_system='')
    error_count = 0
    for i in servers:
        report_servers = ServerReport.objects.filter(ip_address=i.ip, app_id=i.app_id, source=i.source)
        if not report_servers:
            continue
        report_server = report_servers.order_by('-id')[0]
        if ServerReportDetail.objects.filter(warn_status=True, server_report_id=report_server.id).exists():
            error_count += 1

    return error_count


def get_task_list_chart(username, is_superuser):
    install_list = [{'name': u'\u672c\u6708\u5de1\u68c0\u6b21\u6570', 'data': get_check_list(username, is_superuser)}]
    months = get_month_in_year()
    return {'data': install_list, 'categories': [ str(i) + '\xe6\x9c\x88' for i in months ]}


def get_month_in_year():
    u = 0
    months = []
    m = datetime.datetime.now().month
    for i in xrange(1, 13):
        if i > m:
            months.insert(u, i)
            u += 1
        else:
            months.append(i)

    return months


def get_check_list(username, is_superuser):
    date_now = datetime.datetime.now()
    check_report = CheckReport.objects.filter(status='COMPLETE')
    if not is_superuser:
        check_report = check_report.filter(check_task_created_by=username)
    return_data = []
    for i in xrange(12):
        time_start = str(date_now.year) + '-' + '%02d' % date_now.month + '-01 00:00:00'
        time_end = str(date_now.year) + '-' + '%02d' % date_now.month + '-32 00:00:00'
        one_date = check_report.filter(when_created__range=(time_start, time_end)).count()
        return_data.insert(0, one_date)
        date_delay = get_1st_of_last_month(date_now)
        date_now = date_delay

    return return_data


def get_1st_of_last_month(today):
    year = today.year
    month = today.month
    if month == 1:
        month = 12
        year -= 1
    else:
        month -= 1
    res = datetime.datetime(year, month, 1)
    return res


def update_url(request):
    try:
        window_url = request.GET['app_path']
        SysConfig.objects.update_or_create(key='url', defaults={'value': window_url})
        sys_config = SysConfig.objects.filter(key='url')
        if sys_config:
            sys_config.update(value=window_url)
        else:
            SysConfig.objects.create(key='url', value=window_url)
        return render_json({'result': True})
    except Exception as e:
        logger.exception(e)
        return render_json({'result': False})


def get_settings(request):
    try:
        set_obj = GlobalSetting.objects.get(id=1)
        return render_json({'result': True, 'data': set_obj.to_dic()})
    except Exception as e:
        logger.exception(e)
        return render_json({'result': False, 'data': [u'\u7cfb\u7edf\u5f02\u5e38\uff0c\u8bf7\u8054\u7cfb\u7ba1\u7406\u5458']})


def set_settings(request):
    try:
        sys_set = eval(request.body)
        GlobalSetting.objects.filter(id=1).update(config_account=sys_set['config_account'], report_save=sys_set['report_save'])
        return render_json({'result': True})
    except Exception as e:
        logger.exception(e)
        return render_json({'result': False, 'data': [u'\u7cfb\u7edf\u5f02\u5e38\uff0c\u8bf7\u8054\u7cfb\u7ba1\u7406\u5458']})


def search_business_servers(request):
    try:
        filter_obj = eval(request.body)
        if str(filter_obj['type_id']) == '1':
            os_name = 'centos redhat oracle'
        else:
            if str(filter_obj['type_id']) == '2':
                os_name = 'linux suse'
            else:
                os_name = ''
            if not filter_obj['type_id']:
                return render_json({'result': False, 'data': [u'\u8bf7\u5148\u9009\u62e9\u7cfb\u7edf\u7c7b\u578b\uff01']})
            username = request.user.username
            result = get_business_ids_by_user(username)
            if not result['result']:
                logger.error('\xe8\x8e\xb7\xe5\x8f\x96\xe7\x94\xa8\xe6\x88\xb7\xe4\xb8\x9a\xe5\x8a\xa1\xe4\xbf\xa1\xe6\x81\xaf\xe5\xa4\xb1\xe8\xb4\xa5\xef\xbc\x9a%s' % result['data'])
                return render_json({'result': False, 'data': [u'\u83b7\u53d6\u7528\u6237\u4e1a\u52a1\u4fe1\u606f\u5931\u8d25\uff0c\u8bf7\u8054\u7cfb\u7ba1\u7406\u5458']})
            app_ids = result['data']
            bus_hosts = get_hosts_by_apps(app_ids, username, '1', os_name)
            if not bus_hosts['result']:
                logger.error('\xe8\x8e\xb7\xe5\x8f\x96\xe4\xb8\x9a\xe5\x8a\xa1\xe4\xb8\xbb\xe6\x9c\xba\xe4\xbf\xa1\xe6\x81\xaf\xe5\xa4\xb1\xe8\xb4\xa5\xef\xbc\x9a%s' % bus_hosts['data'])
                return render_json({'result': True, 'data': []})
        return_servers = format_host_list(bus_hosts['data'])
        return render_json({'result': True, 'data': return_servers})
    except Exception as e:
        logger.exception(e.message)
        return render_json({'result': False, 'data': [u'\u7cfb\u7edf\u51fa\u9519\uff0c\u8bf7\u8054\u7cfb\u7ba1\u7406\u5458']})


def search_business_topo(request):
    try:
        topo_type = request.GET['topo_type']
        username = request.user.username
        biz_id = request.GET['bk_biz_id']
        checked = request.GET['checked']
        if checked == 'true':
            return render_json([])
        if topo_type == '1':
            topo_result = get_business_topo(biz_id, username)
            if not topo_result['result']:
                logger.exception(topo_result['data'])
                return render_json([])
            if topo_result['data'] and topo_result['data'][0].get('child', []):
                return render_json(topo_result['data'][0]['child'])
            return render_json([])
        os_type_id = request.GET['os_type']
        if str(os_type_id) == '1':
            os_name = 'centos redhat oracle'
        else:
            if str(os_type_id) == '2':
                os_name = 'linux suse'
            else:
                os_name = ''
            username = request.user.username
            module_id = request.GET['bk_inst_id']
            if str(module_id) == '-1':
                return render_json([])
            return_data = get_hosts_by_business_module('', module_id, username, '1', os_name)
            if not return_data['result']:
                logger.error('\xe8\x8e\xb7\xe5\x8f\x96\xe6\xa8\xa1\xe5\x9d\x97\xe4\xb8\x8b\xe4\xb8\xbb\xe6\x9c\xba\xe5\x88\x97\xe8\xa1\xa8\xe5\xa4\xb1\xe8\xb4\xa5\xef\xbc\x9a%s' % return_data['data'])
                return render_json([])
        host_list = format_host_list(return_data['data'])
        return render_json(host_list)
    except Exception as e:
        logger.exception(e)
        return render_json({'result': False, 'data': [u'\u7cfb\u7edf\u51fa\u9519\uff0c\u8bf7\u8054\u7cfb\u7ba1\u7406\u5458']})


def get_all_business(request):
    username = request.user.username
    bus_result = get_business_by_user(username)
    if not bus_result['result']:
        logger.exception(bus_result['data'])
        return {'result': False, 'data': []}
    return_data = format_business(bus_result['data'])
    return render_json({'result': True, 'data': return_data})


def format_business(data):
    return [ {'bk_inst_name': i['bk_biz_name'], 'bk_biz_id': i['bk_biz_id'], 'bk_biz_name': i['bk_biz_name'], 'isParent': True, 'open': False, 'topo_type': 1, 'isSelect': False, 'child': [], 'node_name': i['bk_biz_name'], 'bk_obj_id': 'biz', 'bk_obj_name': 'biz', 'bk_inst_id': i['bk_biz_id']} for i in data
           ]


def search_module_servers(request):
    try:
        os_type_id = request.GET['os_type']
        if str(os_type_id) == '1':
            os_name = 'centos redhat oracle'
        else:
            if str(os_type_id) == '2':
                os_name = 'linux suse'
            else:
                os_name = ''
            username = request.user.username
            module_id = request.GET['bk_inst_id']
            if str(module_id) == '-1':
                return render_json([])
            return_data = get_hosts_by_business_module('', module_id, username, '1', os_name)
            if not return_data['result']:
                logger.error('\xe8\x8e\xb7\xe5\x8f\x96\xe6\xa8\xa1\xe5\x9d\x97\xe4\xb8\x8b\xe4\xb8\xbb\xe6\x9c\xba\xe5\x88\x97\xe8\xa1\xa8\xe5\xa4\xb1\xe8\xb4\xa5\xef\xbc\x9a%s' % return_data['data'])
                return render_json([])
        host_list = format_host_list(return_data['data'])
        return render_json(host_list)
    except Exception as e:
        logger.exception(e)
        return render_json([])


def get_app_check_servers(request):
    try:
        tree_node = json.loads(request.body)
        type_id = request.GET['type_id']
        if str(type_id) == '1':
            os_name = 'centos redhat oracle'
        else:
            if str(type_id) == '2':
                os_name = 'linux suse'
            else:
                os_name = ''
            username = request.user.username
            data = []
            topo_result = get_business_topo(tree_node['bk_biz_id'], username)
            if not topo_result['result']:
                logger.exception(topo_result['data'])
                return render_json([])
        if topo_result['data'] and topo_result['data'][0].get('child', []):
            data = topo_result['data'][0]['child']
        tree_node['child'] = data
        return_data = get_check_servers_children(tree_node, username, os_name)
        return render_json({'result': True, 'data': return_data})
    except Exception as e:
        logger.exception(e)
        return render_json({'result': False, 'data': []})


def format_host_list(host_list, is_checked=False):
    return_data = []
    for i in host_list:
        for x in i['bk_cloud_id']:
            one_obj = {'app_id': i['app_id'], 
               'bk_biz_id': i['app_id'], 'bk_obj_id': 'IP', 'bk_inst_id': -1, 
               'bk_host_id': i['bk_host_id'], 'source_name': x['bk_inst_name'], 'bk_obj_name': 'IP', 
               'child': [], 'checked': is_checked, 'bk_inst_name': i['bk_host_innerip'] + u'(' + x['bk_inst_name'] + u')', 
               'bk_host_innerip': i['bk_host_innerip'], 
               'ip': i['bk_host_innerip'], 'source': x['bk_inst_id'], 
               'bk_os_name': i['bk_os_name'], 'isParent': False}
            if one_obj not in return_data:
                return_data.append(one_obj)

    return return_data


def get_check_servers(request):
    try:
        os_type_id = request.GET['os_type']
        if str(os_type_id) == '1':
            os_name = 'centos redhat oracle'
        elif str(os_type_id) == '2':
            os_name = 'linux suse'
        else:
            os_name = ''
        obj = json.loads(request.body)
        return_data = get_check_servers_children(obj, request.user.username, os_name)
        return render_json({'result': True, 'data': return_data})
    except Exception as e:
        logger.exception(e)
        return render_json({'result': False, 'data': []})


def get_check_servers_children(obj, username, os_name):
    return_data = []
    if 'child' not in obj:
        return []
    for i in obj['child']:
        one_obj = i
        one_obj['checked'] = True
        one_obj['open'] = True
        one_obj['is_open_all'] = True
        if one_obj['bk_obj_name'] != 'IP':
            one_obj['child'] = get_check_servers_children(i, username, os_name)
            if not one_obj['child']:
                one_obj['isParent'] = False
        return_data.append(one_obj)

    if not obj['child']:
        if obj['bk_obj_id'] != 'module':
            return []
        servers = get_hosts_by_business_module('', obj['bk_inst_id'], username, '1', os_name)
        if not servers['result']:
            logger.error('\xe8\x8e\xb7\xe5\x8f\x96\xe6\xa8\xa1\xe5\x9d\x97\xe4\xb8\x8b\xe4\xb8\xbb\xe6\x9c\xba\xe5\x88\x97\xe8\xa1\xa8\xe5\xa4\xb1\xe8\xb4\xa5\xef\xbc\x9a%s' % servers['data'])
            return []
        return_data = format_host_list(servers['data'], True)
    return return_data


def upload_img(request):
    try:
        file_img = request.FILES['upfile']
        content = file_img.read()
        LogoImg.objects.filter(key='logo').update(value=content)
        return render_json({'result': True})
    except Exception as e:
        logger.exception(e)
        return render_json({'result': False, 'data': [u'\u7cfb\u7edf\u5f02\u5e38\uff0c\u8bf7\u8054\u7cfb\u7ba1\u7406\u5458\uff01']})


def show_logo(request):
    try:
        file_one = open(IMG_FILE, 'rb')
        logo_obj, _ = LogoImg.objects.get_or_create(key='logo', defaults={'value': file_one.read()})
        file_one.close()
        photo_data = logo_obj.value
        response = HttpResponse(logo_obj.value, content_type='image/png')
        response['Content-Length'] = len(photo_data)
        return response
    except Exception as e:
        logger.error(e)


def set_default_img(request):
    LogoImg.objects.filter(key='logo').delete()
    return render_json({'result': True})