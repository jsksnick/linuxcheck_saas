# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.9 Stackless 3.1b3 060516 (default, Nov 28 2016, 09:05:13) 
# [GCC 4.4.7 20120313 (Red Hat 4.4.7-17)]
# Embedded file name: /bkdata/vcs2/tmp/linuxcheck_saas-1561098846.95/linuxcheck_saas/src/home_application/celery_tasks.py
# Compiled at: 2019-06-21 14:34:36
"""
celery \xe4\xbb\xbb\xe5\x8a\xa1\xe7\xa4\xba\xe4\xbe\x8b

\xe6\x9c\xac\xe5\x9c\xb0\xe5\x90\xaf\xe5\x8a\xa8celery\xe5\x91\xbd\xe4\xbb\xa4: python  manage.py  celery  worker  --settings=settings
\xe5\x91\xa8\xe6\x9c\x9f\xe6\x80\xa7\xe4\xbb\xbb\xe5\x8a\xa1\xe8\xbf\x98\xe9\x9c\x80\xe8\xa6\x81\xe5\x90\xaf\xe5\x8a\xa8celery\xe8\xb0\x83\xe5\xba\xa6\xe5\x91\xbd\xe4\xbb\xa4\xef\xbc\x9apython  manage.py  celerybeat --settings=settings
"""
import os, threading
from multiprocessing import Process
from collections import defaultdict
from celery import task
from django.db.models import F
from home_application.models import *
from home_application.esb_helper import *
IP_SOURCE_KEY = '{ip}_{source}'
MAX_THREADS = 6

@task()
def run_task(time_set_id, run_op=True):
    """\xe5\xbc\x82\xe6\xad\xa5\xe8\xb0\x83\xe7\x94\xa8\xe4\xbd\x9c\xe4\xb8\x9a\xe5\xb9\xb3\xe5\x8f\xb0\xe6\x89\xa7\xe8\xa1\x8c\xe5\xb7\xa1\xe6\xa3\x80\xe8\x84\x9a\xe6\x9c\xac"""
    celery_time_set = CeleryTimeSet.objects.get(id=time_set_id)
    if celery_time_set.is_deleted:
        celery_time_set.delete()
        return
    check_task = CheckTask.objects.get(celery_time_set_id=time_set_id)
    check_report = CheckReport.objects.create(check_task_id=check_task.id, when_created=str(datetime.datetime.now()).split('.')[0], check_task_name=check_task.name, check_module_id=check_task.check_module_id, check_task_created_by=check_task.created_by, finish_num=0)
    user_name = check_task.created_by
    client = get_client_by_user(user_name)
    all_len = 0
    try:
        ip_list = get_check_server_list(check_task)
        if not ip_list:
            check_report.finish_num = 1
            check_report.save()
            finish_task(all_len, check_report, check_task, celery_time_set, run_op)
            return
        all_len = len(ip_list)
        try:
            app_info = get_business_by_user(user_name)
            if app_info['result']:
                app_id_name_map = {i['bk_biz_id']:i['bk_biz_name'] for i in app_info['data']}
            else:
                logger.error('get_business_by_user error: %s.' % app_info['data'])
                app_id_name_map = {}
        except Exception as e:
            logger.error('get_business_by_user error: %s.' % e.message)
            app_id_name_map = {}

        run_apps, ip_source_source_name_dict = format_check_run_app(ip_list, app_id_name_map)
        check_module_id = check_task.check_module_id
        item_list = CheckItemValue.objects.filter(check_module_id=check_module_id)
        custom_item_list = CustomItemValue.objects.filter(check_module_id=check_module_id).select_related('custom_item')
        check_jobs, perform_jobs, custom_jobs = send_job(user_name, client, run_apps, check_task, check_report, item_list, custom_item_list)
        total_job_num = len(check_jobs) + len(perform_jobs) + len(custom_jobs)
        if not total_job_num:
            check_report.total_job_num = 1
            check_report.finish_num = 1
        else:
            check_report.total_job_num = total_job_num
        check_report.total_num = all_len
        check_report.save()
        if check_jobs:
            check_job_result_manage(client, user_name, ip_source_source_name_dict, check_report, item_list, check_jobs)
        if perform_jobs:
            perform_job_result_manage(client, user_name, ip_source_source_name_dict, check_report, item_list, perform_jobs)
        if custom_jobs:
            custom_job_result_manage(client, user_name, ip_source_source_name_dict, check_report, custom_item_list, custom_jobs)
    except Exception as e:
        logger.exception('run_task error: %s' % e.message)

    finish_task(all_len, check_report, check_task, celery_time_set, run_op)


def check_job_result_manage(client, user_name, ip_source_source_name_dict, check_report, item_list, check_jobs):
    """check\xe7\xb1\xbb\xe5\xb7\xa1\xe6\xa3\x80\xe7\xbb\x93\xe6\x9e\x9c\xe5\xa4\x84\xe7\x90\x86"""

    def _run_thread(_job, _semaphore):
        _semaphore.acquire()
        try:
            try:
                server_report_detail_create_list = list()
                script_result = get_task_ip_log(client, _job['job_id'], user_name)
                for i in script_result:
                    source_name = ip_source_source_name_dict[IP_SOURCE_KEY.format(ip=i['ip'], source=i['source'])]
                    if not i['is_success']:
                        create_server_error_report(check_report.id, i, _job['run_app'], source_name, summary=i['logContent'])
                        continue
                    server_report_detail_create_list += format_check_log_content(i, check_report, source_name, _job['run_app'], item_list)

                if server_report_detail_create_list:
                    ServerReportDetail.objects.bulk_create(server_report_detail_create_list, batch_size=500)
            except BaseException as e:
                logger.exception('check_job_result_manage error: %s, , detail info: %s.' % (e.message, _job))

        finally:
            CheckReport.objects.filter(pk=check_report.id).update(finish_num=F('finish_num') + 1)
            logger.info('check_job_result_manage_finally, app_id\xef\xbc\x9a%s' % _job['run_app']['app_id'])
            _semaphore.release()

    semaphore = threading.BoundedSemaphore(MAX_THREADS)
    threads = []
    for job in check_jobs:
        t = threading.Thread(target=_run_thread, args=(job, semaphore))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()


def perform_job_result_manage(client, user_name, ip_source_source_name_dict, check_report, item_list, perform_jobs):
    """perform\xe7\xb1\xbb\xe5\xb7\xa1\xe6\xa3\x80\xe7\xbb\x93\xe6\x9e\x9c\xe5\xa4\x84\xe7\x90\x86"""

    def _run_thread(_job, _semaphore):
        _semaphore.acquire()
        try:
            try:
                subscibe_detail_create_list = list()
                script_result = get_task_ip_log(client, _job['job_id'], user_name)
                for i in script_result:
                    source_name = ip_source_source_name_dict[IP_SOURCE_KEY.format(ip=i['ip'], source=i['source'])]
                    if not i['is_success']:
                        create_server_error_report(check_report.id, i, _job['run_app'], source_name, summary=i['logContent'])
                        continue
                    subscibe_detail_create_list += format_performs_result(i, source_name, _job['run_app'], item_list, check_report)

                if subscibe_detail_create_list:
                    SubscibeDetail.objects.bulk_create(subscibe_detail_create_list, batch_size=500)
            except BaseException as e:
                logger.exception('perform_job_result_manage error: %s, detail info: %s.' % (e.message, _job))

        finally:
            CheckReport.objects.filter(pk=check_report.id).update(finish_num=F('finish_num') + 1)
            logger.info('perform_job_result_manage_finally, app_id\xef\xbc\x9a%s' % _job['run_app']['app_id'])
            _semaphore.release()

    semaphore = threading.BoundedSemaphore(MAX_THREADS)
    threads = []
    for job in perform_jobs:
        t = threading.Thread(target=_run_thread, args=(job, semaphore))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()


def custom_job_result_manage(client, user_name, ip_source_source_name_dict, check_report, custom_item_list, custom_jobs):
    """custom\xe7\xb1\xbb\xe5\xb7\xa1\xe6\xa3\x80\xe7\xbb\x93\xe6\x9e\x9c\xe5\xa4\x84\xe7\x90\x86"""

    def _run_thread(_job, _semaphore):
        _semaphore.acquire()
        try:
            try:
                custom_report_detail_create_list = list()
                script_result = get_task_ip_log(client, _job['job_id'], user_name)
                for i in script_result:
                    source_name = ip_source_source_name_dict[IP_SOURCE_KEY.format(ip=i['ip'], source=i['source'])]
                    if not i['is_success']:
                        create_server_error_report(check_report.id, i, _job['run_app'], source_name, summary=i['logContent'])
                        continue
                    custom_report_detail_create_list += format_custom_result(i, source_name, _job['run_app'], custom_item_list, check_report)

                if custom_report_detail_create_list:
                    CustomReportDetail.objects.bulk_create(custom_report_detail_create_list, batch_size=500)
            except BaseException as e:
                logger.exception('custom_job_result_manage error: %s, detail info: %s.' % (e.message, _job))

        finally:
            CheckReport.objects.filter(pk=check_report.id).update(finish_num=F('finish_num') + 1)
            logger.info('custom_job_result_manage_finally, app_id\xef\xbc\x9a%s' % _job['run_app']['app_id'])
            _semaphore.release()

    semaphore = threading.BoundedSemaphore(MAX_THREADS)
    threads = []
    for job in custom_jobs:
        t = threading.Thread(target=_run_thread, args=(job, semaphore))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()


def finish_task(all_len, check_report, check_task, time_set, run_op):
    """\xe5\xb7\xa1\xe6\xa3\x80\xe7\xbb\x93\xe6\x9d\x9f\xef\xbc\x8c\xe5\x8f\x91\xe9\x80\x81\xe6\x8a\xa5\xe5\x91\x8a\xe9\x82\xae\xe4\xbb\xb6"""
    try:
        success_len = ServerReport.objects.filter(check_report_id=check_report.id, is_success=True).count()
        check_report = CheckReport.objects.get(pk=check_report.id)
        check_report.error_summary = create_error_summary(check_report)
        check_report.status = u'COMPLETE'
        check_report.report_info = (u'\u672c\u6b21\u5171\u5de1\u68c0{0}\u53f0\u670d\u52a1\u5668\uff0c\u5b8c\u6210{1}\u53f0').format(str(all_len), str(success_len))
        check_report.save()
        report_url = SysConfig.objects.get(key='url').value + '#/reportServer?report_id=' + str(check_report.id)
        mail_content = u"\u4eb2\u7231\u7684\u7ba1\u7406\u5458\uff0c\u4ee5\u4e0b\u662f\u672c\u6b21\u5de1\u68c0\u7684\u7ed3\u679c\u6982\u8981\u62a5\u544a\uff0c\u656c\u8bf7\u67e5\u9605\u3002<br />\u4efb\u52a1\u540d\u79f0: %s <br />\u6267\u884c\u65f6\u95f4\uff1a%s <br />\u4efb\u52a1\u6982\u51b5: %s <br />\u521b\u5efa\u8005\uff1a%s <br />\u8be6\u60c5\u8bf7\u767b\u5f55<a href='%s'>Linux\u5de1\u68c0</a>\u67e5\u770b" % (
         check_task.name, check_report.when_created,
         check_report.report_info, check_task.created_by,
         report_url)
        receivers = check_task.receivers
        title = u'Linux\u5de1\u68c0\u62a5\u544a-' + check_report.when_created
        new_send_email(receivers, title, mail_content)
        if not run_op:
            return
        if time_set.time_type == 'cycle':
            day_interval = time_set.time_interval
            now_time = datetime.datetime.strptime(time_set.run_time, '%Y-%m-%d %H:%M')
            next_date = now_time + datetime.timedelta(days=day_interval)
            time_set.run_time = datetime.datetime.strftime(next_date, '%Y-%m-%d %H:%M')
            time_set.save()
            run_task.apply_async(args=[time_set.id], eta=next_date)
    except Exception as e:
        logger.exception('finish_task error: %s' % e.message)


def create_error_summary(check_report):
    """\xe5\xb7\xa1\xe6\xa3\x80\xe7\xbb\x93\xe6\x9d\x9f\xe6\x97\xb6\xef\xbc\x8c\xe5\x9c\xa8\xe5\xb7\xa1\xe6\xa3\x80\xe6\x8a\xa5\xe5\x91\x8a\xe8\xa1\xa8\xe4\xb8\xad\xef\xbc\x8c\xe7\x94\x9f\xe6\x88\x90\xe9\x94\x99\xe8\xaf\xaf\xe6\xb1\x87\xe6\x80\xbb\xe4\xbf\xa1\xe6\x81\xaf\xef\xbc\x8c\xe6\x96\xb9\xe4\xbe\xbf\xe5\x90\x8e\xe7\xbb\xad\xe6\x9f\xa5\xe7\x9c\x8b\xe3\x80\x81\xe5\xaf\xbc\xe5\x87\xba
    'name': 0,
    'item': [{
        'display': '123',
        'type': 'dict',
        'value': {
            "a": 123,
            "b": {'type': 'dict',
                'value': {
                    'c': 1,
                    'd': 2}}},
        'way': '>',
        'compare': '12'},
    """
    try:
        server_reports = ServerReport.objects.filter(check_report_id=check_report.id, is_success=True)
        if not server_reports.exists():
            return json.dumps([])
        check_item_value = CheckItemValue.objects.filter(check_module_id=check_report.check_module_id)
        item_value_dict = {i.check_item_id:i.value for i in check_item_value}
        custom_item_value = CustomItemValue.objects.filter(check_module_id=check_report.check_module_id)
        custom_item_value_dict = {i.custom_item_id:i.value for i in custom_item_value}
        error_summary = []
        for server_report in server_reports:
            try:
                error_obj = {'name': server_report.ip_address, 'item': []}
                if item_value_dict:
                    check_errors = ServerReportDetail.objects.filter(warn_status=True, server_report_id=server_report.id).select_related('check_item')
                    for check_error in check_errors:
                        error_obj['item'].append({'display': check_error.check_item.cn_name, 'value': check_error.value, 
                           'way': check_error.check_item.compare_way, 
                           'compare': item_value_dict[check_error.check_item.id]})

                    perform_errors = SubscibeDetail.objects.filter(is_warn=True, server_report_id=server_report.id).select_related('check_item')
                    for perform_error in perform_errors:
                        if perform_error.value != 'null' and perform_error.check_item.value_type == 'form' and eval(perform_error.value):
                            error_obj['item'].append({'display': perform_error.check_item.cn_name, 'type': 'list', 
                               'value': [ i for i in eval(perform_error.value) if i['is_warn'] ], 'keys': [ {i: i} for i in eval(perform_error.value)[0] ], 'way': perform_error.check_item.compare_way, 
                               'compare': item_value_dict[perform_error.check_item.id]})
                        else:
                            error_obj['item'].append({'display': perform_error.check_item.cn_name, 'value': perform_error.value, 
                               'way': perform_error.check_item.compare_way, 
                               'compare': item_value_dict[perform_error.check_item.id]})

                if custom_item_value_dict:
                    custom_errors = CustomReportDetail.objects.filter(is_warn=True, server_report_id=server_report.id).select_related('custom_item')
                    for custom_error in custom_errors:
                        error_obj['item'].append({'display': custom_error.custom_item.cn_name, 'value': custom_error.value, 
                           'way': custom_error.custom_item.compare_way, 
                           'compare': custom_item_value_dict[custom_error.custom_item.id]})

                if not error_obj['item']:
                    continue
                else:
                    error_summary.append(error_obj)
            except Exception as e:
                logger.exception('create_error_summary error: %s, report_id: %s, report_name: %s, server_ip: %s' % (
                 e.message, check_report.id, check_report.check_task_name, server_report.ip_address))
                continue

        return json.dumps(error_summary)
    except Exception as e:
        logger.exception('create_error_summary error: %s, report_id: %s, report_name: %s' % (
         e.message, check_report.id, check_report.check_task_name))
        return json.dumps([])


def format_check_run_app(ip_list, app_id_name_map):
    """\xe6\xa0\xb9\xe6\x8d\xae\xe4\xb8\x9a\xe5\x8a\xa1\xe5\x88\x92\xe5\x88\x86\xe4\xb8\xbb\xe6\x9c\xba"""
    app_host_dict = defaultdict(list)
    ip_source_source_name_dict = dict()
    for i in ip_list:
        host_info = {'ip': i['ip'], 'source': i['source'], 'source_name': i['source_name']}
        if host_info not in app_host_dict[i['app_id']]:
            app_host_dict[i['app_id']].append(host_info)
        ip_source_source_name_dict[IP_SOURCE_KEY.format(ip=i['ip'], source=i['source'])] = i['source_name']

    run_apps = []
    for app_id, host_list in app_host_dict.items():
        run_apps.append({'app_id': app_id, 'ip_list': host_list, 'app_name': app_id_name_map.get(app_id, '')})

    return (run_apps, ip_source_source_name_dict)


def send_job(user_name, client, run_apps, check_task, check_report, item_list, custom_item_list):
    """\xe8\xb0\x83\xe7\x94\xa8\xe4\xbd\x9c\xe4\xb8\x9a\xe5\xb9\xb3\xe5\x8f\xb0\xe4\xb8\x8b\xe5\x8f\x91\xe5\xb7\xa1\xe6\xa3\x80\xe4\xbd\x9c\xe4\xb8\x9a\xef\xbc\x8c\xe8\xbf\x94\xe5\x9b\x9e\xe4\xbd\x9c\xe4\xb8\x9a\xe5\xae\x9e\xe4\xbe\x8bid"""
    os_type = check_task.check_module.os_type
    script_account = check_task.script_account
    try:
        if item_list.exists():
            check_jobs = send_check_job(run_apps, client, os_type, user_name, script_account, check_report, item_list)
            perform_jobs = run_perform_check(run_apps, client, user_name, check_report, script_account, os_type, item_list)
        else:
            check_jobs = list()
            perform_jobs = list()
        custom_jobs = run_custom_check(run_apps, client, user_name, check_report, script_account, custom_item_list)
        return (
         check_jobs, perform_jobs, custom_jobs)
    except Exception as e:
        logger.exception('send_job error: %s' % e.message)
        return ([], [], [])


def create_server_report(check_report_id, i, app, is_success, source_name, summary=''):
    """\xe5\x8f\x91\xe9\x80\x81\xe4\xbd\x9c\xe4\xb8\x9a\xe5\xa4\xb1\xe8\xb4\xa5\xe8\xb0\x83\xe7\x94\xa8\xef\xbc\x8c\xe5\x88\x9b\xe5\xbb\xba\xe4\xb8\xbb\xe6\x9c\xba\xe6\x8a\xa5\xe5\x91\x8a"""
    return ServerReport(check_report_id=check_report_id, ip_address=i['ip'], app_id=app['app_id'], source=i['source'], source_name=source_name, is_success=is_success, summary=summary, app_name=app['app_name'])


def create_server_error_report(check_report_id, i, app, source_name, summary=''):
    """\xe8\x8e\xb7\xe5\x8f\x96\xe4\xbd\x9c\xe4\xb8\x9a\xe6\x97\xa5\xe5\xbf\x97\xe5\xa4\xb1\xe8\xb4\xa5\xe8\xb0\x83\xe7\x94\xa8\xef\xbc\x8c\xe5\x88\x9b\xe5\xbb\xba\xe4\xb8\xbb\xe6\x9c\xba\xe6\x8a\xa5\xe5\x91\x8a"""
    ServerReport.objects.update_or_create(check_report_id=check_report_id, ip_address=i['ip'], source=i['source'], app_id=app['app_id'], source_name=source_name, app_name=app['app_name'], defaults={'is_success': False, 'summary': summary})


def format_check_log_content(i, check_report, source_name, app, item_list):
    """check \xe7\xb1\xbb\xe5\xb7\xa1\xe6\xa3\x80\xe7\xbb\x93\xe6\x9e\x9c\xe5\xa4\x84\xe7\x90\x86"""
    server_report = ServerReport.objects.get_or_create(ip_address=i['ip'], source=i['source'], app_id=app['app_id'], check_report_id=check_report.id, source_name=source_name, defaults={'is_success': True, 'app_name': app['app_name']})[0]
    info_list = [ i for i in i['logContent'].strip('\n').split('\n') if i ]
    server_report_detail_create_list = list()
    for info_content in info_list:
        try:
            new_dict = info_content.split('=')
            check_items = item_list.filter(check_item__name=new_dict[0]).select_related('check_item')
            if not check_items.exists():
                continue
            check_item = check_items.first().check_item
            value_dict = new_dict[1].split('@@')
            if len(value_dict) == 1:
                status = False
            else:
                status = value_dict[1] == '1'
            new_value = value_dict[0].replace('^', '=').replace('&gt;', '>').replace('&lt;', '<') if check_item.value_type == 'table' else value_dict[0]
            server_report_detail_create_list.append(ServerReportDetail(check_item_id=check_item.id, server_report_id=server_report.id, value=new_value, warn_status=status))
        except Exception as e:
            logger.exception('format_check_log_content error: %s, log\xef\xbc\x9a%s' % (
             e.message, server_report.ip_address + ':' + info_content))

    return server_report_detail_create_list


def send_check_job(run_apps, client, os_type, user_name, script_account, check_report, item_list):
    """\xe5\x8f\x91\xe9\x80\x81check\xe7\xb1\xbb\xe5\xb7\xa1\xe6\xa3\x80, \xe8\xbf\x94\xe5\x9b\x9e\xe4\xbd\x9c\xe4\xb8\x9a\xe5\xae\x9e\xe4\xbe\x8b"""
    try:
        script_content = create_check_script(item_list, os_type)
        if not script_content:
            return []
        check_jobs = list()
        server_report_create_list = list()
        for run_app in run_apps:
            result = fast_execute_script(run_app, client, user_name, script_account, script_content)
            if not result['result']:
                for i in run_app['ip_list']:
                    server_report_create_list.append(create_server_report(check_report.id, i, run_app, False, i['source_name'], result['error']))

            else:
                check_jobs.append({'job_id': result['job_id'], 'run_app': run_app})

        if server_report_create_list:
            ServerReport.objects.bulk_create(server_report_create_list)
        return check_jobs
    except Exception as e:
        logger.exception('send_check_job error: %s' % e.message)
        return []


def run_custom_check(run_apps, client, user_name, check_report, script_account, custom_item_list):
    """\xe5\x8f\x91\xe9\x80\x81custom\xe7\xb1\xbb\xe5\xb7\xa1\xe6\xa3\x80, \xe8\xbf\x94\xe5\x9b\x9e\xe4\xbd\x9c\xe4\xb8\x9a\xe5\xae\x9e\xe4\xbe\x8b"""
    try:
        if not run_apps:
            return []
        else:
            if not custom_item_list.exists():
                return []
            script_content = format_custom_script(custom_item_list)
            custom_jobs = list()
            for run_app in run_apps:
                result = fast_execute_script(run_app, client, user_name, script_account, script_content)
                if not result['result']:
                    logger.error('run_custom_check error: %s, app_id: %s, app_name: %s' % (
                     result['error'], run_app['app_id'], run_app['app_name']))
                    continue
                else:
                    custom_jobs.append({'job_id': result['job_id'], 'run_app': run_app})

            return custom_jobs

    except Exception as e:
        logger.exception('run_custom_check error: %s' % e.message)
        return []


def format_custom_result(i, source_name, app, item_list, check_report):
    """custom \xe7\xb1\xbb\xe5\xb7\xa1\xe6\xa3\x80\xe7\xbb\x93\xe6\x9e\x9c\xe5\xa4\x84\xe7\x90\x86"""
    server_report = ServerReport.objects.get_or_create(ip_address=i['ip'], source=i['source'], app_id=app['app_id'], check_report_id=check_report.id, source_name=source_name, defaults={'is_success': True, 'app_name': app['app_name']})[0]
    log_list = [ u for u in i['logContent'].split('\n') if u ]
    custom_report_detail_create_list = list()
    for u in log_list:
        try:
            custom_item_obj = CustomItem.objects.filter(name=u.split('=')[0])
            if not custom_item_obj.exists():
                continue
            custom_item = custom_item_obj.first()
            custom_value = item_list.filter(custom_item__name=u.split('=')[0]).first()
            try:
                real_value = float(u.split('=')[1].strip(' '))
                compare_value = float(custom_value.value)
                compare_text = '%s%s%s' % (real_value, custom_item.compare_way, compare_value)
            except:
                real_value = u.split('=')[1].strip(' ')
                compare_value = custom_value.value
                compare_text = "'%s'=='%s'" % (real_value, compare_value)

            logger.error(compare_text)
            custom_report_detail_create_list.append(CustomReportDetail(custom_item_id=custom_item.id, value=u.split('=')[1].strip(' '), server_report_id=server_report.id, is_warn=not eval(compare_text)))
        except Exception as e:
            logger.exception('format_custom_result error: %s, log\xef\xbc\x9a%s' % (
             e.message, server_report.ip_address + ':' + u))

    return custom_report_detail_create_list


def format_custom_script(item_list):
    script_content = ('\n').join([ i.custom_item.script_content for i in item_list ])
    return '#!/bin/bash\n#Author:Allen\n#Descripttion:Collect server information\n#company:canway\n\n################################################################\nexport LANG="en_US.UTF-8"\n    \n' + script_content


def run_perform_check(run_apps, client, user_name, check_report, script_account, os_type, item_list):
    """\xe5\x8f\x91\xe9\x80\x81perform\xe7\xb1\xbb\xe5\xb7\xa1\xe6\xa3\x80, \xe8\xbf\x94\xe5\x9b\x9e\xe4\xbd\x9c\xe4\xb8\x9a\xe5\xae\x9e\xe4\xbe\x8b"""
    try:
        if not run_apps:
            return []
        else:
            item_list = item_list.filter(check_item__item_type='performs')
            if not item_list.exists():
                return []
            script_content = ScriptContent.objects.get(name='performs', os_type=os_type).content
            perform_jobs = list()
            for run_app in run_apps:
                result = fast_execute_script(run_app, client, user_name, script_account, script_content)
                if not result['result']:
                    logger.error('run_perform_check error: %s, app_id: %s, app_name: %s' % (
                     result['error'], run_app['app_id'], run_app['app_name']))
                    for i in run_app['ip_list']:
                        ServerReport.objects.update_or_create(check_report_id=check_report.id, ip_address=i['ip'], source=i['source'], app_id=run_app['app_id'], defaults={'is_success': False, 
                           'summary': result['error']})

                    continue
                else:
                    perform_jobs.append({'job_id': result['job_id'], 'run_app': run_app})

            return perform_jobs

    except Exception as e:
        logger.exception('run_perform_check error: %s' % e.message)
        return []


def format_performs_result(i, source_name, app, item_list, check_report):
    """performs\xe7\xb1\xbb\xe5\xb7\xa1\xe6\xa3\x80\xe7\xbb\x93\xe6\x9e\x9c\xe5\xa4\x84\xe7\x90\x86"""
    server_report = ServerReport.objects.get_or_create(ip_address=i['ip'], source=i['source'], app_id=app['app_id'], check_report_id=check_report.id, source_name=source_name, defaults={'is_success': True, 'app_name': app['app_name']})[0]
    item_list = item_list.filter(check_item__item_type='performs')
    log_list = [ u for u in i['logContent'].split('\n') if u ]
    subscibe_detail_create_list = list()
    for u in log_list:
        try:
            obj = u.split('=')
            check_items = item_list.filter(check_item__name=obj[0]).select_related('check_item')
            if not check_items.exists():
                continue
            is_warn = False
            check_item_obj = check_items.first().check_item
            check_module_obj = check_items.first()
            compare_value = '' if not check_module_obj.value else (float(check_module_obj.value) if '%' not in check_module_obj.value else float(check_module_obj.value.split('%')[0]))
            if check_item_obj.value_type == 'form':
                values = obj[1].strip(';').split(';')
                if values[0] == 'null':
                    real_value = values[0]
                    subscibe_detail_create_list.append(SubscibeDetail(server_report_id=server_report.id, value=real_value, check_item_id=check_item_obj.id, when_created='', is_warn=is_warn))
                    continue
                else:
                    real_value = [ {'name': o.split('@')[0], 'value': o.split('@')[1]} for o in values ]
                    is_warn = False
                    for m in real_value:
                        if not compare_value:
                            m['is_warn'] = False
                        elif check_item_obj.compare_way == '<=':
                            if float(m['value']) > compare_value:
                                is_warn = True
                                m['is_warn'] = True
                            else:
                                m['is_warn'] = False
                        elif float(m['value']) < compare_value:
                            is_warn = True
                            m['is_warn'] = True
                        else:
                            m['is_warn'] = False

                    subscibe_detail_create_list.append(SubscibeDetail(server_report_id=server_report.id, value=real_value, check_item_id=check_item_obj.id, when_created='', is_warn=is_warn))
            else:
                real_value = obj[1]
                if not compare_value:
                    is_warn = False
                elif check_item_obj.compare_way == '<=':
                    if float(real_value) > compare_value:
                        is_warn = True
                elif float(real_value) < compare_value:
                    is_warn = True
                subscibe_detail_create_list.append(SubscibeDetail(server_report_id=server_report.id, value=real_value, check_item_id=check_item_obj.id, when_created='', is_warn=is_warn))
        except Exception as e:
            logger.exception('format_performs_result error: %s, log\xef\xbc\x9a%s' % (
             e.message, server_report.ip_address + ':' + u))

    return subscibe_detail_create_list


def create_check_script(item_list, os_type):
    """\xe6\xa0\xb9\xe6\x8d\xae\xe4\xb8\xbb\xe6\x9c\xba\xe7\xb1\xbb\xe5\x9e\x8b\xe4\xbb\xa5\xe5\x8f\x8a\xe5\xb7\xa1\xe6\xa3\x80\xe9\xa1\xb9\xe5\x8a\xa8\xe6\x80\x81\xe7\x94\x9f\xe6\x88\x90check\xe5\xb7\xa1\xe6\xa3\x80\xe8\x84\x9a\xe6\x9c\xac"""
    if os_type == '1':
        from normal_check_script import check_items
    else:
        from suse_check_script import check_items
    item_list = item_list.filter(check_item__item_type__in=['check', 'info']).select_related('check_item')
    if not item_list.exists():
        return ''
    check_script = check_items['title']['content'] + '\n'
    try:
        for item in item_list:
            item_in_dict = check_items[item.check_item.name]
            if item_in_dict.get('has_param'):
                if item.value:
                    content = item_in_dict['content'] % item.value
                else:
                    content = item_in_dict['content'] % item_in_dict['default_param']
            else:
                content = item_in_dict['content']
            check_script += content + '\n'

        return check_script
    except Exception as e:
        logger.exception('create_check_script error: %s' % e.message)
        return ''


@task
def delete_file(file_path):
    os.remove(file_path)