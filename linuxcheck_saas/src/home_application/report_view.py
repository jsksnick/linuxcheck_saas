# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.9 Stackless 3.1b3 060516 (default, Nov 28 2016, 09:05:13) 
# [GCC 4.4.7 20120313 (Red Hat 4.4.7-17)]
# Embedded file name: /bkdata/vcs2/tmp/linuxcheck_saas-1561098846.95/linuxcheck_saas/src/home_application/report_view.py
# Compiled at: 2019-06-21 14:34:36
from common.mymako import render_json
import json
from home_application.models import *
from common.log import logger
from account.decorators import login_exempt
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction

def get_report_list(request):
    try:
        filter_obj = json.loads(request.body)
        report_list = CheckReport.objects.filter(when_created__range=[
         filter_obj['start_time'] + ' 00:00:00', filter_obj['end_time'] + ' 23:59:59'], check_task_name__icontains=filter_obj['task_name']).exclude(status='COMPLETE', serverreport=None)
        if not request.user.is_superuser:
            report_list = report_list.filter(check_task_created_by=request.user.username)
        is_checked = report_list.filter(status='RUNNING').count() > 0
        return_data = [ {'id': i.id, 'task_name': i.check_task_name, 'when_created': i.when_created, 'summary': i.report_info, 'status': i.status, 'schedule': ('{:.2%}').format(float(i.finish_num) / i.total_job_num)} for i in report_list.order_by('-id')
                      ]
        return render_json({'result': True, 'is_checked': is_checked, 'data': return_data})
    except Exception as e:
        logger.exception(e)
        return render_json({'result': False, 'data': [u'\u7cfb\u7edf\u5f02\u5e38\uff0c\u8bf7\u8054\u7cfb\u7ba1\u7406\u5458']})

    return


def delete_report(request):
    try:
        if not request.user.is_superuser:
            return render_json({'result': False, 'data': [u'\u975e\u7ba1\u7406\u5458\uff0c\u4e0d\u5141\u8bb8\u5220\u9664\u62a5\u544a\uff01']})
        else:
            filter_obj = json.loads(request.body)
            with transaction.atomic():
                check_report = CheckReport.objects.get(id=filter_obj['id'])
                log = OperationLog()
                log.create_log(check_report, None, 'delete', request.user.username)
                check_report.delete()
            return render_json({'result': True})

    except Exception as e:
        logger.exception(e)
        return render_json({'result': False, 'data': [u'\u7cfb\u7edf\u5f02\u5e38\uff0c\u8bf7\u8054\u7cfb\u7ba1\u7406\u5458']})

    return


def get_report_server_by_id(request):
    """\xe6\xa0\xb9\xe6\x8d\xae\xe6\x8a\xa5\xe5\x91\x8aid\xe8\x8e\xb7\xe5\x8f\x96\xe6\x8a\xa5\xe5\x91\x8a\xe8\xaf\xa6\xe6\x83\x85"""
    try:
        report_id = request.GET['report_id']
        if int(report_id) == 0:
            report_list = CheckReport.objects.filter(status='COMPLETE').exclude(serverreport=None)
            if not request.user.is_superuser:
                report_list = report_list.filter(check_task_created_by=request.user.username)
            if report_list.exists():
                check_report = report_list.order_by('-id').first()
            else:
                return render_json({'result': False, 'data': [u'\u8fd8\u672a\u6267\u884c\u8fc7\u5de1\u68c0\uff0c\u6682\u65e0\u62a5\u544a\uff01']})
        else:
            check_report = CheckReport.objects.get(pk=report_id)
        return_data = _get_report_server_by_id(check_report)
        return render_json(return_data)
    except Exception as e:
        logger.exception(e.message)
        return render_json({'result': False, 'data': [u'\u7cfb\u7edf\u5f02\u5e38\uff0c\u8bf7\u8054\u7cfb\u7ba1\u7406\u5458']})

    return


def _get_report_server_by_id(check_report):
    """\xe6\x8f\x90\xe5\x8f\x96\xe5\x87\xba\xe8\x8e\xb7\xe5\x8f\x96\xe6\x8a\xa5\xe5\x91\x8a\xe5\x85\xac\xe5\x85\xb1\xe6\x96\xb9\xe6\xb3\x95"""
    report_server_list = ServerReport.objects.filter(check_report_id=check_report.id)
    return_data = {'server_list': [], 'name': check_report.check_task_name, 'when_created': check_report.when_created, 'agent_server': []}
    return_data = get_report_server_error_summary(report_server_list, return_data)
    question_list = []
    return {'result': True, 'data': return_data, 'question_list': question_list}


@csrf_exempt
@login_exempt
def get_job_result_by_api(request):
    """\xe6\xa0\xb9\xe6\x8d\xae\xe6\x8a\xa5\xe5\x91\x8aid\xe8\x8e\xb7\xe5\x8f\x96\xe6\x8a\xa5\xe5\x91\x8a\xe8\xaf\xa6\xe6\x83\x85"""
    try:
        report_id = json.loads(request.body).get('report_id', '')
        if not report_id:
            return render_json({'result': False, 'data': u'\u6ca1\u6709\u62a5\u544aid'})
        check_report = CheckReport.objects.get(pk=report_id)
        if check_report.status == 'RUNNING':
            return render_json({'result': True, 'status': 'RUNNING'})
        return_data = _get_report_server_by_id(check_report)
        for server_obj in return_data['data']['server_list']:
            if not server_obj['is_success']:
                continue
            menu_list = _get_report_server_detail_by_id(server_obj)
            error_list, summary = get_error_server_list(server_obj['id'])
            server_obj['server_detail_report'] = {'result': True, 'menu_list': menu_list, 'error_list': error_list, 
               'summary': summary}

        return render_json({'result': True, 'status': 'COMPLETE', 'data': return_data})
    except Exception as e:
        logger.exception(e.message)
        return render_json({'result': False, 'data': e.message})


def get_report_error_summary_by_id(request):
    """\xe6\xa0\xb9\xe6\x8d\xae\xe6\x8a\xa5\xe5\x91\x8aid\xe8\x8e\xb7\xe5\x8f\x96\xe9\x94\x99\xe8\xaf\xaf\xe8\xaf\xa6\xe6\x83\x85"""
    try:
        report_id = request.GET['report_id']
        report_obj = CheckReport.objects.get(pk=report_id)
        summary_data = json.loads(report_obj.error_summary)
        return_data = {'server_list': [], 'name': report_obj.check_task_name, 'when_created': report_obj.when_created}
        report_server_list = ServerReport.objects.filter(check_report_id=report_id)
        return_data = get_report_server_error_summary(report_server_list, return_data, is_need_server_list=False)
        return render_json({'result': True, 'data': return_data, 'summary_data': summary_data})
    except Exception as e:
        logger.exception(e.message)
        return render_json({'result': False, 'data': [u'\u7cfb\u7edf\u5f02\u5e38\uff0c\u8bf7\u8054\u7cfb\u7ba1\u7406\u5458']})


def get_question_pie_chart(report_id):
    all_details = ServerReportDetail.objects.filter(server_report__check_report_id=report_id, warn_status=True)
    perf_details = SubscibeDetail.objects.filter(server_report__check_report_id=report_id, is_warn=True)
    menus = ItemMenu.objects.exclude(name='\xe7\xb3\xbb\xe7\xbb\x9f\xe6\x80\xa7\xe8\x83\xbd\xe4\xbf\xa1\xe6\x81\xaf').values('child_name').order_by('child_order').distinct()
    return_data = []
    for i in menus:
        one_obj = {'name': i['child_name'], 'y': all_details.filter(check_item__menu_name=i['child_name']).count()}
        return_data.append(one_obj)

    return_data.append({'name': '\xe7\xb3\xbb\xe7\xbb\x9f\xe6\x80\xa7\xe8\x83\xbd\xe4\xbf\xa1\xe6\x81\xaf', 'y': len(perf_details)})
    return return_data


def get_report_server_summary(server_report):
    """\xe5\xbe\x97\xe5\x88\xb0\xe6\xaf\x8f\xe4\xb8\xaa\xe4\xb8\xbb\xe6\x9c\xba\xe7\x9a\x84\xe6\xa6\x82\xe8\xbf\xb0"""
    all_details = ServerReportDetail.objects.filter(server_report_id=server_report.id)
    all_sub_details = SubscibeDetail.objects.filter(server_report_id=server_report.id)
    warn_details = all_details.filter(warn_status=True)
    warn_sub_details = all_sub_details.filter(is_warn=True)
    detail_return = []
    menus = ItemMenu.objects.all().values('child_name').order_by('child_order').distinct()
    custom_details = CustomReportDetail.objects.filter(server_report_id=server_report.id)
    all_count = all_details.count() + custom_details.count() + all_sub_details.count()
    error_count = 0
    for i in menus:
        one_details = warn_details.filter(check_item__menu_name=i['child_name'])
        two_details = warn_sub_details.filter(check_item__menu_name=i['child_name'])
        if one_details or two_details:
            detail_return.append(('{0}\xef\xbc\x9a{1}\xe9\xa1\xb9\xe4\xb8\x8d\xe5\x90\x88\xe6\xa0\xbc').format(i['child_name'], one_details.count() + two_details.count()))
            error_count += one_details.count() + two_details.count()

    custom_error_count = custom_details.filter(is_warn=True).count()
    if custom_error_count:
        error_count += custom_error_count
        detail_return.append(('\xe8\x87\xaa\xe5\xae\x9a\xe4\xb9\x89\xe9\xa1\xb9\xef\xbc\x9a{0}\xe9\xa1\xb9\xe4\xb8\x8d\xe5\x90\x88\xe6\xa0\xbc').format(custom_error_count))
    summary = ("\xe6\x9c\xac\xe6\xac\xa1\xe5\xb7\xa1\xe6\xa3\x80\xe5\x85\xb1\xe5\x8f\x91\xe7\x8e\xb0<span class='error_item'>{0}</span>\xe9\xa1\xb9\xe5\xbc\x82\xe5\xb8\xb8").format(error_count)
    if error_count == 0:
        summary = "<span class='success_item'>\xe6\x9c\xac\xe6\xac\xa1\xe5\xb7\xa1\xe6\xa3\x80\xe6\x9c\xaa\xe5\x8f\x91\xe7\x8e\xb0\xe9\x97\xae\xe9\xa2\x98</span>"
    return (
     summary, detail_return)


def get_report_server_error_summary(report_server_list, return_data, is_need_server_list=True):
    """\xe8\x8e\xb7\xe5\x8f\x96\xe4\xb8\xbb\xe6\x9c\xba\xe6\x8a\xa5\xe5\x91\x8a\xe7\x9a\x84\xe6\xa6\x82\xe8\xa6\x81"""
    server_count = report_server_list.count()
    server_error_count = report_server_list.filter(is_success=False).count()
    server_success_list = report_server_list.filter(is_success=True)
    check_errors = ServerReportDetail.objects.filter(server_report__in=server_success_list, warn_status=True)
    perform_errors = SubscibeDetail.objects.filter(server_report__in=server_success_list, is_warn=True)
    custom_errors = CustomReportDetail.objects.filter(server_report__in=server_success_list, is_warn=True)
    q_all = check_errors.count() + perform_errors.count() + custom_errors.count()
    q_error = ''
    s = 0
    for i in report_server_list:
        if check_errors.filter(server_report_id=i.id).exists() or perform_errors.filter(server_report_id=i.id).exists() or custom_errors.filter(server_report_id=i.id).exists():
            s += 1
        if is_need_server_list:
            one_obj = {'app': i.app_name if i.app_name else i.app_id, 'source': i.source, 'ip_address': i.ip_address, 
               'id': i.id, 'summary': i.summary, 
               'is_success': i.is_success, 'details': [], 'source_name': i.source_name}
            if i.is_success:
                summary, details = get_report_server_summary(i)
                one_obj['summary'] = summary
                one_obj['details'] = details
            return_data['server_list'].append(one_obj)

    s_error = (u'\u672c\u6b21\u5171\u5de1\u68c0{0}\u53f0\u670d\u52a1\u5668\uff0c{1}\u53f0\u5de1\u68c0\u5931\u8d25\uff0c{2}\u53f0\u5b58\u5728\u5f02\u5e38\uff0c\u5171{3}\u9879\u5f02\u5e38.').format(server_count, server_error_count, s, q_all)
    return_data = dict(return_data, **{'q_error': q_error, 's_error': s_error})
    return return_data


@login_exempt
def get_report_server_detail_by_id(request):
    try:
        server_obj = json.loads(request.body)
        menu_list = _get_report_server_detail_by_id(server_obj)
        error_list, summary = get_error_server_list(server_obj['id'])
        return render_json({'result': True, 'menu_list': menu_list, 'error_list': error_list, 'summary': summary})
    except Exception as e:
        logger.exception(e)
        return render_json({'result': False, 'data': [u'\u7cfb\u7edf\u5f02\u5e38\uff0c\u8bf7\u8054\u7cfb\u7ba1\u7406\u5458\uff01']})


def _get_report_server_detail_by_id(server_obj):
    """ \xe6\x8f\x90\xe5\x8f\x96\xe5\x87\xba\xe8\x8e\xb7\xe5\x8f\x96\xe5\xad\x90\xe9\xa1\xb5\xe9\x9d\xa2\xe4\xbf\xa1\xe6\x81\xaf\xe5\x85\xac\xe5\x85\xb1\xe5\x87\xbd\xe6\x95\xb0"""
    server_details = ServerReportDetail.objects.filter(server_report_id=server_obj['id']).order_by('check_item_id')
    menu_list = []
    check_module_id = ServerReport.objects.get(pk=server_obj['id']).check_report.check_module_id
    item_list = CheckItemValue.objects.filter(check_module_id=check_module_id).select_related('check_item')
    item_names = [ i.check_item.menu_name for i in item_list ]
    menus = ItemMenu.objects.filter(child_name__in=set(item_names)).exclude(name='\xe7\xb3\xbb\xe7\xbb\x9f\xe6\x80\xa7\xe8\x83\xbd\xe4\xbf\xa1\xe6\x81\xaf').values('name').order_by('order').distinct()
    for i in menus:
        menu_two = ItemMenu.objects.filter(name=i['name'], child_name__in=set(item_names)).order_by('child_order')
        one_obj = {'name': i['name'], 
           'is_show': False, 'menu_two': [ {'name': x.child_name, 'order': x.child_order, 'details': get_server_details_by_menu(item_list, server_details, x)} for x in menu_two
                     ]}
        menu_list.append(one_obj)

    custom_obj = get_custom_item_details(check_module_id, server_obj['id'])
    perform_details = get_performs_details(check_module_id, server_obj['id'])
    if perform_details:
        menu_list.append(perform_details)
    if custom_obj:
        menu_list.append(custom_obj)
    return menu_list


def get_custom_item_details(check_module_id, server_obj_id):
    custom_item_value = CustomItemValue.objects.filter(check_module_id=check_module_id)
    custom_item_details = CustomReportDetail.objects.filter(server_report_id=server_obj_id).select_related('custom_item')
    details = []
    for u in custom_item_details:
        item_value = custom_item_value.get(custom_item_id=u.custom_item.id).value
        one_obj = {'menu_name': '', 
           'cn_name': u.custom_item.cn_name, 
           'real_value': u.value, 'is_warn': u.is_warn, 
           'value_type': '', 'compare_way': u.custom_item.compare_way, 
           'value': item_value, 'warn_class': 'error_text'}
        details.append(one_obj)

    if details:
        return {'name': '\xe8\x87\xaa\xe5\xae\x9a\xe4\xb9\x89\xe9\xa1\xb9', 'is_show': False, 'menu_two': [{'name': '', 'details': details}]}
    else:
        return


def get_performs_details(check_module_id, server_obj_id):
    performs_details = SubscibeDetail.objects.filter(server_report_id=server_obj_id).select_related('check_item')
    details = []
    for u in performs_details:
        check_item_obj = u.check_item
        item_value_obj = CheckItemValue.objects.get(check_item_id=check_item_obj.id, check_module_id=check_module_id)
        if check_item_obj.severity_level == '1':
            warn_class = 'error_text'
        elif check_item_obj.severity_level == '2':
            warn_class = 'warn-text'
        else:
            warn_class = 'normal-text'
        if u.value == 'null':
            one_obj = {'menu_name': '', 'cn_name': check_item_obj.cn_name, 'real_value': u.value, 'is_warn': u.is_warn, 'value_type': check_item_obj.value_type, 'warn_class': warn_class, 'value': item_value_obj.value, 'compare_way': check_item_obj.compare_way}
        else:
            one_obj = {'menu_name': '', 'cn_name': check_item_obj.cn_name, 'real_value': eval(u.value) if check_item_obj.value_type == 'form' else u.value, 
               'is_warn': u.is_warn, 
               'value_type': check_item_obj.value_type, 
               'warn_class': warn_class, 'value': item_value_obj.value, 'compare_way': check_item_obj.compare_way}
        details.append(one_obj)

    if details:
        return {'name': '\xe7\xb3\xbb\xe7\xbb\x9f\xe6\x80\xa7\xe8\x83\xbd\xe4\xbf\xa1\xe6\x81\xaf', 'is_show': False, 'is_performs': True, 'menu_two': [{'name': '', 'details': details}]}
    else:
        return


def get_error_server_list(server_id):
    server_error_details = ServerReportDetail.objects.filter(server_report_id=server_id, warn_status=True).order_by('check_item_id')
    perf_error_details = SubscibeDetail.objects.filter(server_report_id=server_id, is_warn=True).order_by('check_item_id')
    h = server_error_details.filter(check_item__severity_level='1').count() + perf_error_details.filter(check_item__severity_level='1').count()
    m = server_error_details.filter(check_item__severity_level='2').count() + perf_error_details.filter(check_item__severity_level='2').count()
    l = server_error_details.filter(check_item__severity_level='3').count() + perf_error_details.filter(check_item__severity_level='3').count()
    return_data = [{'name': '\xe9\xab\x98', 'y': h, 'color': '#ea4335'}, {'name': '\xe4\xb8\xad', 'y': m, 'color': '#fbbc05'}, {'name': '\xe4\xbd\x8e', 'y': l, 'color': '#f5fc88'}]
    if h:
        level = '\xe8\xbe\x83\xe5\xb7\xae'
    elif m:
        level = '\xe4\xb8\xad\xe7\xad\x89'
    elif l:
        level = '\xe8\x89\xaf\xe5\xa5\xbd'
    else:
        level = '\xe4\xbc\x98\xe7\xa7\x80'
    summary = ('\xe6\x80\xbb\xe4\xbd\x93\xe5\x81\xa5\xe5\xba\xb7\xe6\x80\xa7{4}\xef\xbc\x8c\xe5\x85\xb1\xe6\x9c\x89{0}\xe9\xa1\xb9\xe9\x97\xae\xe9\xa2\x98\xef\xbc\x8c{1}\xe9\xa1\xb9\xe9\x97\xae\xe9\xa2\x98\xe7\xad\x89\xe7\xba\xa7\xe4\xb8\xba\xe9\xab\x98\xef\xbc\x8c{2}\xe9\xa1\xb9\xe9\x97\xae\xe9\xa2\x98\xe7\xad\x89\xe7\xba\xa7\xe4\xb8\xba\xe4\xb8\xad\xef\xbc\x8c{3}\xe9\xa1\xb9\xe9\x97\xae\xe9\xa2\x98\xe7\xad\x89\xe7\xba\xa7\xe4\xb8\xba\xe4\xbd\x8e').format(h + m + l, h, m, l, level)
    return (
     return_data, summary)


def get_server_details_by_menu(item_list, server_details, menu):
    return_data = []
    for u in server_details.filter(check_item__menu_name=menu.child_name).select_related('check_item'):
        item_value = item_list.get(check_item__name=u.check_item.name).value
        if u.check_item.severity_level == '1':
            warn_class = 'error_text'
        elif u.check_item.severity_level == '2':
            warn_class = 'warn-text'
        else:
            warn_class = 'normal-text'
        one_obj = {'menu_name': u.check_item.menu_name, 'cn_name': u.check_item.cn_name, 
           'real_value': u.value, 'is_warn': u.warn_status, 
           'value_type': u.check_item.value_type, 'compare_way': u.check_item.compare_way, 
           'value': item_value, 'warn_class': warn_class}
        return_data.append(one_obj)

    return return_data