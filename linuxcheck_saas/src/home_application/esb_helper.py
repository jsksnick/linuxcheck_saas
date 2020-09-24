# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.9 Stackless 3.1b3 060516 (default, Nov 28 2016, 09:05:13) 
# [GCC 4.4.7 20120313 (Red Hat 4.4.7-17)]
# Embedded file name: /bkdata/vcs2/tmp/linuxcheck_saas-1561098846.95/linuxcheck_saas/src/home_application/esb_helper.py
# Compiled at: 2019-06-21 14:34:36
from blueking.component.shortcuts import get_client_by_request, get_client_by_user
from conf.default import APP_ID, APP_TOKEN, BK_PAAS_HOST
import base64, time
from common.log import logger
import requests
from esb.client import get_esb_client
import httplib2, json, sys
from esb.new_client import get_new_esb_client
reload(sys)
sys.setdefaultencoding('utf8')

def fast_execute_script_1(check_app, client, user_name, execute_account, script_content, param_content=None, script_timeout=1000):
    kwargs = {'app_code': APP_ID, 
       'app_secret': APP_TOKEN, 
       'app_id': check_app['app_id'], 
       'username': user_name, 
       'content': base64.b64encode(script_content), 
       'ip_list': check_app['ip_list'], 
       'type': 1, 
       'account': execute_account, 
       'script_param': param_content, 
       'script_timeout': script_timeout}
    result = client.job.fast_execute_script(kwargs)
    if result['result']:
        time.sleep(5)
        script_result = get_task_ip_log(client, result['data']['taskInstanceId'], user_name)
        return {'result': True, 'data': script_result}
    else:
        return {'result': False, 'data': result['message']}


def fast_execute_script(check_app, client, user_name, execute_account, script_content, param_content=None, script_timeout=1000):
    """\xe8\xb0\x83\xe7\x94\xa8\xe4\xbd\x9c\xe4\xb8\x9a\xe5\xb9\xb3\xe5\x8f\xb0\xef\xbc\x8c\xe6\x89\xa7\xe8\xa1\x8c\xe4\xbd\x9c\xe4\xb8\x9a\xef\xbc\x8c\xe8\xbf\x94\xe5\x9b\x9e\xe4\xbd\x9c\xe4\xb8\x9a\xe5\xae\x9e\xe4\xbe\x8bid"""
    kwargs = {'app_code': APP_ID, 
       'app_secret': APP_TOKEN, 
       'app_id': check_app['app_id'], 
       'username': user_name, 
       'content': base64.b64encode(script_content), 
       'ip_list': check_app['ip_list'], 
       'type': 1, 
       'account': execute_account, 
       'script_param': param_content, 
       'script_timeout': script_timeout}
    result = client.job.fast_execute_script(kwargs)
    if result['result']:
        return {'result': True, 'job_id': result['data']['taskInstanceId']}
    else:
        return {'result': False, 'error': result['message']}


def get_task_ip_log(client, task_instance_id, user_name, count=0):
    kwargs = {'app_code': APP_ID, 
       'app_secret': APP_TOKEN, 
       'username': user_name, 
       'task_instance_id': int(task_instance_id)}
    result = client.job.get_task_ip_log(kwargs)
    if result['result']:
        if result['data'][0]['isFinished']:
            log_content = []
            for i in result['data'][0]['stepAnalyseResult']:
                if i['resultType'] != 9:
                    log_contents = [ {'ip': u['ip'], 'logContent': i['resultTypeText'], 'source': u['source'], 'is_success': False} for u in i['ipLogContent']
                                   ]
                else:
                    log_contents = [ {'ip': u['ip'], 'logContent': u['logContent'], 'source': u['source'], 'is_success': True} for u in i['ipLogContent']
                                   ]
                log_content += log_contents

            return log_content
        time.sleep(10)
        return get_task_ip_log(client, task_instance_id, user_name)
    else:
        count += 1
        if count > 5:
            return ''
        time.sleep(10)
        return get_task_ip_log(client, task_instance_id, user_name, count)


def send_email(to, subject, content, content_type='HTML'):
    try:
        if not to:
            return
        else:
            logger.error(u'\u5f00\u59cb\u53d1\u9001\u90ae\u4ef6')
            http = httplib2.Http()
            http.disable_ssl_certificate_validation = True
            body = {'subject': subject, 'to': to, 'content': content, 'content_type': content_type, 'app_code': APP_ID, 'app_secret': APP_TOKEN, 
               'username': APP_ID}
            headers = {'Content-type': 'application/json'}
            url = ('{0}/api/c/compapi/common/send_email/').format(BK_PAAS_HOST)
            response, content = http.request(url, 'POST', headers=headers, body=json.dumps(body))
            data_dic = json.loads(content)
            if data_dic['result']:
                logger.error(u'\u90ae\u4ef6\u53d1\u9001\u6210\u529f')
                return
            logger.error(u'\u90ae\u4ef6\u53d1\u9001\u5931\u8d25')
            logger.error(data_dic['message'])
            return

    except Exception as e:
        logger.exception(e)


def new_send_email(receiver, title, content):
    try:
        logger.error(u'\u5f00\u59cb\u53d1\u9001\u90ae\u4ef6')
        esb_client = get_new_esb_client()
        result = esb_client.call('cmsi', 'send_mail', receiver=receiver, title=title, content=content)
        if result['result']:
            logger.error(u'\u90ae\u4ef6\u53d1\u9001\u6210\u529f')
            return
        logger.error(u'\u90ae\u4ef6\u53d1\u9001\u5931\u8d25')
        logger.error(result['message'])
        return
    except Exception as e:
        logger.exception(e)


def call_api_by_http(api_path, kwargs, username, is_issue=True, request_way='POST'):
    headers = {'Content-type': 'application/json'}
    url = '%s/%s' % (BK_PAAS_HOST, api_path.strip('/'))
    if request_way == 'GET':
        res = requests.get(url, params=json.dumps(kwargs), headers=headers, verify=False)
    else:
        res = requests.post(url, data=json.dumps(kwargs), headers=headers, verify=False)
    if res.status_code == 200:
        content = json.loads(res.content)
        if content['result']:
            return {'result': True, 'data': content['data']}
        return {'result': False, 'data': content['message']}
    else:
        return {'result': False, 'data': res.status_code}


def get_business_by_user(username):
    kwargs = {'bk_app_code': APP_ID, 
       'bk_app_secret': APP_TOKEN, 
       'bk_username': username}
    res = call_api_by_http('/api/c/compapi/v2/cc/search_business/', kwargs, username)
    if res['result']:
        user_business_list = [ {'bk_biz_id': i['bk_biz_id'], 'bk_biz_maintainer': i['bk_biz_maintainer'], 'bk_biz_name': i['bk_biz_name']} for i in res['data']['info'] if username in i['bk_biz_maintainer'].split(',')
                             ]
        return {'result': True, 'data': user_business_list}
    else:
        return {'result': False, 'data': res['data']}


def get_business_ids_by_user(username):
    kwargs = {'bk_app_code': APP_ID, 
       'bk_app_secret': APP_TOKEN, 
       'bk_username': username}
    res = call_api_by_http('/api/c/compapi/v2/cc/search_business/', kwargs, username)
    if res['result']:
        user_business_ids = [ i['bk_biz_id'] for i in res['data']['info'] if username in i['bk_biz_maintainer'].split(',') ]
        return {'result': True, 'data': user_business_ids}
    else:
        return {'result': False, 'data': res['data']}


def get_business_idle(business_id, business_name, username, topo_type=True, check_status=False):
    url = '/api/c/compapi/v2/cc/search_set'
    kwargs = {'app_code': APP_ID, 
       'app_secret': APP_TOKEN, 
       'bk_biz_id': business_id, 
       'bk_username': username, 
       'condition': {'bk_set_name': u'\u7a7a\u95f2\u673a\u6c60'}, 'fields': [
                'bk_set_id'], 
       'page': {'limit': 1, 'sort': 'bk_set_name', 'start': 0}}
    res = call_api_by_http(url, kwargs, username, True, 'POST')
    if not res['result']:
        return {'result': False, 'data': res['data']}
    return get_idle_modules(res['data']['info'][0], business_id, business_name, username, topo_type, check_status)


def get_idle_modules(set_obj, app_id, app_name, username, topo_type=True, check_status=False):
    url = '/api/c/compapi/v2/cc/search_module'
    kwargs = {'app_code': APP_ID, 
       'app_secret': APP_TOKEN, 
       'bk_biz_id': app_id, 
       'bk_set_id': set_obj['bk_set_id'], 
       'bk_username': username, 
       'condition': {'bk_module_name': u'\u7a7a\u95f2\u673a'}, 'fields': [
                'bk_module_id', 'bk_module_name'], 
       'page': {'limit': 10, 'sort': 'bk_module_name', 'start': 0}}
    res = call_api_by_http(url, kwargs, username, True, 'POST')
    if not res['result']:
        return {'result': False, 'data': u'\u83b7\u53d6\u7a7a\u95f2\u673a\u5f02\u5e38'}
    return_data = {'bk_inst_id': set_obj['bk_set_id'], 'bk_inst_name': u'\u7a7a\u95f2\u673a\u6c60', 'bk_biz_id': app_id, 'bk_biz_name': app_name, 
       'bk_obj_id': 'set', 'bk_obj_name': u'\u7a7a\u95f2\u673a\u6c60', 'open': False, 'topo_type': 2, 
       'isSelect': False, 'node_name': app_name + '_\xe7\xa9\xba\xe9\x97\xb2\xe6\x9c\xba\xe6\xb1\xa0', 'checked': check_status, 'chkDisabled': check_status, 
       'child': [ {'bk_inst_id': i['bk_module_id'], 'bk_biz_id': app_id, 'bk_inst_name': i['bk_module_name'], 'topo_type': 2, 'bk_obj_id': 'module', 'bk_obj_name': u'\u6a21\u5757', 'child': [], 'default': 0, 'isParent': topo_type, 'open': False, 'isSelect': False, 'bk_biz_name': app_name, 'checked': check_status, 'chkDisabled': check_status, 'node_name': app_name + '_' + i['bk_module_name']} for i in res['data']['info']
              ]}
    return {'result': True, 'data': return_data}


def get_business_topo(business_id, username, level=-1, topo_type=True, check_status=False):
    api_path = '/api/c/compapi/v2/cc/search_biz_inst_topo/'
    kwargs = {'bk_app_code': APP_ID, 
       'bk_app_secret': APP_TOKEN, 
       'bk_username': username, 
       'bk_biz_id': business_id, 
       'level': level}
    res = call_api_by_http(api_path, kwargs, username)
    if res['result']:
        return_data = format_business_topo(res['data'], business_id, res['data'][0]['bk_inst_name'], res['data'][0]['bk_inst_name'], topo_type, check_status)
        idle_result = get_business_idle(business_id, res['data'][0]['bk_inst_name'], username, topo_type, check_status)
        if idle_result['result']:
            return_data[0]['child'].append(idle_result['data'])
        return {'result': True, 'data': return_data}
    else:
        return {'result': False, 'data': res['data']}


def format_business_topo(data, bk_biz_id, bk_biz_name, node_name, topo_type=True, check_status=False):
    return_data = []
    for i in data:
        if i['bk_obj_id'] == 'biz':
            node_name = i['bk_inst_name']
        else:
            node_name = '%s_%s' % (node_name, i['bk_inst_name'])
        if not topo_type and i['bk_obj_name'] == 'module':
            tmp = dict(i, **{'isParent': False, 'bk_biz_id': bk_biz_id, 'bk_biz_name': bk_biz_name, 'open': False, 'topo_type': 2, 
               'isSelect': False, 'node_name': node_name, 'checked': check_status, 'chkDisabled': check_status})
        else:
            tmp = dict(i, **{'isParent': True, 'bk_biz_id': bk_biz_id, 'bk_biz_name': bk_biz_name, 'open': False, 'topo_type': 2, 
               'isSelect': False, 'node_name': node_name, 'checked': check_status, 'chkDisabled': check_status})
        tmp['child'] = format_business_topo(tmp['child'], bk_biz_id, bk_biz_name, node_name, topo_type, check_status)
        return_data.append(tmp)

    return return_data


def get_hosts_by_business_module(business_id, module_id, username, host_type, os_name):
    business_filter = [{'field': 'bk_biz_id', 'operator': '$eq', 'value': int(business_id)}] if business_id else []
    module_filter = [{'field': 'bk_module_id', 'operator': '$eq', 'value': int(module_id)}] if module_id else []
    host_filter = [{'field': 'bk_os_type', 'operator': '$eq', 'value': host_type}] if host_type == '1' or host_type == '2' else []
    if os_name:
        if 'suse' in os_name:
            host_filter.append({'field': 'bk_os_name', 'operator': '$in', 'value': ['linux suse']})
        else:
            host_filter.append({'field': 'bk_os_name', 'operator': '$in', 'value': ['linux redhat', 'linux centos', 'linux oracle']})
    kwargs = {'bk_app_code': APP_ID, 'bk_app_secret': APP_TOKEN, 
       'bk_username': username, 
       'condition': [
                   {'bk_obj_id': 'biz', 
                      'fields': [], 'condition': business_filter},
                   {'bk_obj_id': 'host', 
                      'fields': [], 'condition': host_filter},
                   {'bk_obj_id': 'module', 
                      'fields': [], 'condition': module_filter}]}
    return search_host(kwargs, username)


def get_hosts_by_apps(app_ids, username, host_type, os_name):
    business_filter = [{'field': 'bk_biz_id', 'operator': '$in', 'value': app_ids}] if app_ids else []
    host_filter = [{'field': 'bk_os_type', 'operator': '$eq', 'value': host_type}] if host_type == '1' or host_type == '2' else []
    if os_name:
        if 'suse' in os_name:
            host_filter.append({'field': 'bk_os_name', 'operator': '$in', 'value': ['linux suse']})
        else:
            host_filter.append({'field': 'bk_os_name', 'operator': '$in', 'value': ['linux redhat', 'linux centos', 'linux oracle']})
    kwargs = {'bk_app_code': APP_ID, 'bk_app_secret': APP_TOKEN, 
       'bk_username': username, 
       'condition': [
                   {'bk_obj_id': 'biz', 
                      'fields': [], 'condition': business_filter},
                   {'bk_obj_id': 'host', 
                      'fields': [], 'condition': host_filter},
                   {'bk_obj_id': 'module', 
                      'fields': [], 'condition': []}]}
    return search_host(kwargs, username)


def search_host(kwargs, username):
    res = call_api_by_http('/api/c/compapi/v2/cc/search_host/', kwargs, username)
    if not res['result']:
        return {'result': False, 'data': res['data']}
    data = []
    for i in res['data']['info']:
        one_obj = i['host']
        os_name = format_linux_os_name(one_obj['bk_os_name'])
        if not os_name:
            continue
        os_version = filter_linux_os_version(str(one_obj['bk_os_version']))
        if not os_version:
            continue
        one_obj['app_id'] = i['biz'][0]['bk_biz_id']
        one_obj['bk_biz_id'] = i['biz'][0]['bk_biz_id']
        one_obj['is_checked'] = False
        one_obj['bk_os_name'] = os_name
        one_obj['app_name'] = i['biz'][0]['bk_biz_name']
        data.append(one_obj)

    return_data = filter_no_agent(data, username)
    return {'result': True, 'data': return_data}


def filter_no_agent(data, username):
    kwargs = {'bk_app_code': APP_ID, 
       'bk_app_secret': APP_TOKEN, 
       'bk_username': username, 
       'bk_supplier_id': 0, 
       'hosts': [ {'ip': i['bk_host_innerip'], 'bk_cloud_id': i['bk_cloud_id'][0]['bk_inst_id']} for i in data
              ]}
    res = call_api_by_http('/api/c/compapi/v2/gse/get_agent_status/', kwargs, username)
    if not res['result']:
        return []
    return_data = []
    for i in data:
        key = (u'{0}:{1}').format(i['bk_cloud_id'][0]['bk_inst_id'], i['bk_host_innerip'])
        if res['data'][key]['bk_agent_alive']:
            return_data.append(i)

    return return_data


def format_linux_os_version(os_version):
    if os_version.startswith('5'):
        return '5'
    else:
        if os_version.startswith('6'):
            return '6'
        if os_version.startswith('7'):
            return '7'
        return ''


def filter_linux_os_version(os_version):
    if not os_version:
        return False
    else:
        os_version = float(('.').join(os_version.split('.')[:2]))
        if os_version >= 5.0:
            return True
        return False


def format_linux_os_name(os_name):
    if 'centos' in os_name.lower():
        return 'centos'
    if 'redhat' in os_name:
        return 'rhel'
    if 'suse' in os_name:
        return 'suse'
    if 'oracle' in os_name:
        return 'oracle'
    return ''


def get_business_topo_by_user(username):
    bus_result = get_business_by_user(username)
    if not bus_result['result']:
        return {'result': False, 'data': 'get business info error'}
    return_data = []
    for bus_obj in bus_result['data']:
        topo_result = get_business_topo(bus_obj['bk_biz_id'], username)
        if not topo_result['result']:
            return {'result': False, 'data': 'get business topo info error'}
        return_data.append(topo_result['data'][0])

    return {'result': True, 'data': return_data}


def get_dynamic_group(username, app_id_list):
    api_path = '/api/c/compapi/v2/cc/search_custom_query/'
    return_data = []
    for app_obj in app_id_list:
        kwargs = {'bk_app_code': APP_ID, 'bk_app_secret': APP_TOKEN, 
           'bk_username': username, 
           'bk_biz_id': int(app_obj['app_id']), 
           'condition': {'name': {'$regex': ''}}, 'start': 0, 
           'limit': 200}
        res = call_api_by_http(api_path, kwargs, username)
        if not res['result']:
            logger.exception(res['data'])
        elif res['data']['info']:
            return_data += [ {'app_id': i['bk_biz_id'], 'app_name': app_obj['app_name'], 'create_user': i['create_user'], 'group_name': i['name'], 'group_id': i['id'], 'is_checked': False, 'type': 'group'} for i in res['data']['info']
                           ]

    return return_data


def get_hosts_by_group(username, app_id, group_id, os_list):
    api_path = '/api/c/compapi/v2/cc/get_custom_query_data/'
    return_data = []
    start_num = 0
    limit_num = 200
    while True:
        kwargs = {'bk_app_code': APP_ID, 'bk_app_secret': APP_TOKEN, 
           'bk_username': username, 
           'bk_biz_id': app_id, 
           'id': group_id, 
           'start': start_num, 
           'limit': limit_num}
        res = call_api_by_http(api_path, kwargs, username)
        if not res['result']:
            logger.exception(res['data'])
            return return_data
        return_data += res['data']['info']
        if res['data']['count'] <= limit_num:
            break
        start_num += 200
        limit_num += 200

    data = []
    for i in return_data:
        if not i['host']['bk_os_type'] == '1':
            continue
        one_obj = i['host']
        if os_list and one_obj['bk_os_name'] not in os_list:
            continue
        os_name = format_linux_os_name(one_obj['bk_os_name'])
        if not os_name:
            continue
        os_version = filter_linux_os_version(str(one_obj['bk_os_version']))
        if not os_version:
            continue
        one_obj['bk_os_name'] = os_name
        one_obj['app_id'] = i['biz'][0]['bk_biz_id']
        one_obj['bk_biz_id'] = i['biz'][0]['bk_biz_id']
        one_obj['app_name'] = i['biz'][0]['bk_biz_name']
        one_obj['is_checked'] = False
        data.append(one_obj)

    return_data = filter_no_agent(data, username)
    return return_data


def get_hosts_by_node(username, node_obj, os_list):
    field_name = 'bk_%s_id' % node_obj['bk_obj_id'] if node_obj['bk_obj_id'] in ('biz',
                                                                                 'set',
                                                                                 'module') else 'bk_inst_id'
    host_filter = [{'field': 'bk_os_type', 'operator': '$eq', 'value': '1'}]
    if os_list:
        host_filter.append({'field': 'bk_os_name', 'operator': '$in', 'value': os_list})
    if node_obj['bk_obj_id'] == 'biz':
        condition = [
         {'bk_obj_id': node_obj['bk_obj_id'], 
            'fields': [], 'condition': [
                        {'field': field_name, 
                           'operator': '$in', 
                           'value': [
                                   node_obj['bk_inst_id']]}]},
         {'bk_obj_id': 'host', 
            'fields': [], 'condition': host_filter}]
    else:
        condition = [
         {'bk_obj_id': 'biz', 
            'fields': [], 'condition': []},
         {'bk_obj_id': node_obj['bk_obj_id'], 
            'fields': [], 'condition': [
                        {'field': field_name, 
                           'operator': '$in', 
                           'value': [
                                   node_obj['bk_inst_id']]}]},
         {'bk_obj_id': 'host', 
            'fields': [], 'condition': host_filter}]
    kwargs = {'bk_app_code': APP_ID, 
       'bk_app_secret': APP_TOKEN, 
       'bk_username': username, 
       'condition': condition}
    return search_host(kwargs, username)


def get_check_server_list(check_obj):
    if check_obj.select_type == 'ip':
        return eval(check_obj.ip_list)
    return_data = []
    server_list = []
    if int(check_obj.check_module.os_type) == 1:
        os_list = [
         'linux redhat', 'linux centos', 'linux oracle']
    elif int(check_obj.check_module.os_type) == 2:
        os_list = [
         'linux suse']
    else:
        os_list = []
    if check_obj.select_type == 'group':
        group_list = eval(check_obj.group_list)
        for group_obj in group_list:
            server_list += get_hosts_by_group(check_obj.created_by, group_obj['app_id'], group_obj['group_id'], os_list)

    else:
        if check_obj.select_type == 'topo':
            node_list = eval(check_obj.topo_list)
            server_list = []
            for node_obj in node_list:
                res = get_hosts_by_node(check_obj.created_by, node_obj, os_list)
                if not res['result']:
                    logger.exception(res['data'])
                    continue
                server_list += res['data']

        ip_list = []
        for server_obj in server_list:
            obj = {'ip': server_obj['bk_host_innerip'], 'source': server_obj['bk_cloud_id'][0]['bk_inst_id']}
            if obj not in ip_list:
                ip_list.append(obj)
                return_data.append({'app_id': server_obj['bk_biz_id'], 
                   'app_name': server_obj['app_name'], 'source': server_obj['bk_cloud_id'][0]['bk_inst_id'], 
                   'source_name': server_obj['bk_cloud_id'][0]['bk_inst_name'], 
                   'server_name': server_obj['bk_os_name'], 
                   'ip': server_obj['bk_host_innerip']})

    return return_data