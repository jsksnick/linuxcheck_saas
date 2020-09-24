# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.9 Stackless 3.1b3 060516 (default, Nov 28 2016, 09:05:13) 
# [GCC 4.4.7 20120313 (Red Hat 4.4.7-17)]
# Embedded file name: /bkdata/vcs2/tmp/linuxcheck_saas-1561098846.95/linuxcheck_saas/src/home_application/views.py
# Compiled at: 2019-06-21 14:34:36
from common.mymako import render_mako_context
from home_application.sys_view import *
from home_application.task_view import *
from home_application.report_view import *
from home_application.custom_item_view import *
from home_application.module_view import *
from home_application.export_view import *

def home(request):
    """
    \xe9\xa6\x96\xe9\xa1\xb5
    """
    return render_mako_context(request, '/home_application/js_factory.html')


@login_exempt
def export_page(request):
    config_id = request.GET['config_id']
    sys_config = SysConfig.objects.get(id=config_id)
    html_content = sys_config.value.replace('&amp;', '&').replace('&gt;', '>').replace('&quot;', '"').replace('&#039;', "\\'").replace('&lt;', '<').replace('&nbsp;', ' ').replace('\n', '').replace('\r', '').strip()
    sys_config.delete()
    return render_mako_context(request, '/home_application/export_report_server.html', {'html_content': html_content})