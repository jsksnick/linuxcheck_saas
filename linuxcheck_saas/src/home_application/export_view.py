# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.9 Stackless 3.1b3 060516 (default, Nov 28 2016, 09:05:13) 
# [GCC 4.4.7 20120313 (Red Hat 4.4.7-17)]
# Embedded file name: /bkdata/vcs2/tmp/linuxcheck_saas-1561098846.95/linuxcheck_saas/src/home_application/export_view.py
# Compiled at: 2019-06-21 14:34:36
from common.log import logger
from common.mymako import render_json
from django.http import HttpResponse
import pdfkit
from home_application.models import SysConfig, CheckReport
from conf.default import BK_PAAS_HOST, APP_ID, SITE_URL
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def export_check_server(request):
    try:
        content = request.POST.get('content')
        config = SysConfig.objects.create(key='export_server', value=content)
        report_id = request.GET.get('report_id', '0')
        ip_address = ''
        if request.GET.get('ip'):
            ip_address = request.GET['ip'].replace('.', '_') + '-'
        if report_id == '0':
            check_report = CheckReport.objects.last()
        else:
            check_report = CheckReport.objects.get(id=report_id)
        file_name = check_report.check_task_name + '-' + ip_address + check_report.when_created.replace('-', '_').replace(' ', '').replace(':', '') + '.pdf'
        file_name = file_name.replace(' ', '_')
        file_url = BK_PAAS_HOST + SITE_URL + ('export_page/?config_id={0}').format(config.id)
        options = {'page-size': 'A4', 
           'encoding': 'UTF-8', 
           'javascript-delay': '5000', 
           'margin-top': '0', 
           'margin-bottom': '0', 
           'margin-left': '0', 
           'margin-right': '0', 
           'quiet': ''}
        config = pdfkit.configuration(wkhtmltopdf='/usr/local/bin/wkhtmltopdf')
        pdf_file = pdfkit.from_url(file_url, False, options=options, configuration=config)
        return download_file(pdf_file, file_name)
    except Exception as e:
        logger.exception(e)
        return render_json({'result': False, 'data': [u'\u7cfb\u7edf\u5f02\u5e38\uff0c\u8bf7\u8054\u7cfb\u7ba1\u7406\u5458\uff01']})


@csrf_exempt
def export_check_error_summary(request):
    try:
        content = request.POST.get('content')
        config = SysConfig.objects.create(key='export_check_error_summary', value=content)
        report_id = request.GET['report_id']
        check_report = CheckReport.objects.get(id=report_id)
        file_name = check_report.check_task_name + '-' + check_report.when_created.replace('-', '_').replace(' ', '').replace(':', '') + '-error_summary' + '.pdf'
        file_url = BK_PAAS_HOST + SITE_URL + ('export_page/?config_id={0}').format(config.id)
        options = {'page-size': 'A4', 
           'encoding': 'UTF-8', 
           'javascript-delay': '5000', 
           'margin-top': '0', 
           'margin-bottom': '0', 
           'margin-left': '0', 
           'margin-right': '0', 
           'quiet': ''}
        config = pdfkit.configuration(wkhtmltopdf='/usr/local/bin/wkhtmltopdf')
        pdf_file = pdfkit.from_url(file_url, False, options=options, configuration=config)
        return download_file(pdf_file, file_name)
    except Exception as e:
        logger.exception(e)
        return render_json({'result': False, 'data': [u'\u7cfb\u7edf\u5f02\u5e38\uff0c\u8bf7\u8054\u7cfb\u7ba1\u7406\u5458\uff01']})


def download_file(file_buffer, file_name):
    response = HttpResponse(file_buffer, content_type='APPLICATION/OCTET-STREAM')
    response['Content-Disposition'] = 'attachment; filename=' + file_name.encode('utf8')
    response['Content-Length'] = len(file_buffer)
    return response