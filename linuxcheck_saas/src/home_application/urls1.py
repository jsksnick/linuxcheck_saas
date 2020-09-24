# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.9 Stackless 3.1b3 060516 (default, Nov 28 2016, 09:05:13) 
# [GCC 4.4.7 20120313 (Red Hat 4.4.7-17)]
# Embedded file name: /bkdata/vcs2/tmp/linuxcheck_saas-1561098846.95/linuxcheck_saas/src/home_application/urls.py
# Compiled at: 2019-06-21 14:34:36
stmts (2)
     0. sstmt
        import_from (5)
             0.  L.   3         0  LOAD_CONST               -1
             1.                 3  LOAD_CONST               ('patterns',)
             2.                 6  IMPORT_NAME           0  'django.conf.urls'
             3. importlist
                alias (2)
                     0.                 9  IMPORT_FROM           1  'patterns'
                     1. store
                                       12  STORE_NAME            1  'patterns'
             4.                15  POP_TOP          
     1. sstmt
        assign (2)
             0. expr
                call (55)
                     0. expr
                         L.   5        16  LOAD_NAME             1  'patterns'
                     1. expr
                         L.   6        19  LOAD_CONST               'home_application.views'
                     2. expr
                         L.   8        22  LOAD_CONST               ('^$', 'home')
                     3. expr
                         L.   9        25  LOAD_CONST               ('^export_page/', 'export_page')
                     4. expr
                         L.  11        28  LOAD_CONST               ('^get_count_obj$', 'get_count_obj')
                     5. expr
                         L.  12        31  LOAD_CONST               ('^update_url$', 'update_url')
                     6. expr
                         L.  15        34  LOAD_CONST               ('^get_all_business$', 'get_all_business')
                     7. expr
                         L.  16        37  LOAD_CONST               ('^search_business_servers$', 'search_business_servers')
                     8. expr
                         L.  17        40  LOAD_CONST               ('^search_business_topo/$', 'search_business_topo')
                     9. expr
                         L.  18        43  LOAD_CONST               ('^search_module_servers/$', 'search_module_servers')
                    10. expr
                         L.  19        46  LOAD_CONST               ('^get_check_servers$', 'get_check_servers')
                    11. expr
                         L.  20        49  LOAD_CONST               ('^get_app_check_servers$', 'get_app_check_servers')
                    12. expr
                         L.  23        52  LOAD_CONST               ('^get_task_option$', 'get_task_option')
                    13. expr
                         L.  24        55  LOAD_CONST               ('^get_user_mail$', 'get_user_mail')
                    14. expr
                         L.  25        58  LOAD_CONST               ('^create_task$', 'create_task')
                    15. expr
                         L.  26        61  LOAD_CONST               ('^create_check_job_by_api$', 'create_check_job_by_api')
                    16. expr
                         L.  27        64  LOAD_CONST               ('^get_task_list$', 'get_task_list')
                    17. expr
                         L.  28        67  LOAD_CONST               ('^get_check_task_by_api$', 'get_check_task_by_api')
                    18. expr
                         L.  29        70  LOAD_CONST               ('^run_task_now$', 'run_task_now')
                    19. expr
                         L.  30        73  LOAD_CONST               ('^modify_task$', 'modify_task')
                    20. expr
                         L.  31        76  LOAD_CONST               ('^task_clone$', 'task_clone')
                    21. expr
                         L.  32        79  LOAD_CONST               ('^delete_task$', 'delete_task')
                    22. expr
                         L.  33        82  LOAD_CONST               ('^search_dynamic_group_list$', 'search_dynamic_group_list')
                    23. expr
                         L.  34        85  LOAD_CONST               ('^check_app_topo$', 'check_app_topo')
                    24. expr
                         L.  35        88  LOAD_CONST               ('^get_check_topo$', 'get_check_topo')
                    25. expr
                         L.  36        91  LOAD_CONST               ('^search_app_topo$', 'search_app_topo')
                    26. expr
                         L.  39        94  LOAD_CONST               ('^get_module_item_list$', 'get_module_item_list')
                    27. expr
                         L.  40        97  LOAD_CONST               ('^search_module_list$', 'search_module_list')
                    28. expr
                         L.  41       100  LOAD_CONST               ('^get_module_list$', 'get_module_list')
                    29. expr
                         L.  42       103  LOAD_CONST               ('^create_module$', 'create_module')
                    30. expr
                         L.  43       106  LOAD_CONST               ('^modify_module$', 'modify_module')
                    31. expr
                         L.  44       109  LOAD_CONST               ('^delete_module$', 'delete_module')
                    32. expr
                         L.  47       112  LOAD_CONST               ('^get_item_list', 'get_item_list')
                    33. expr
                         L.  48       115  LOAD_CONST               ('^create_custom_item', 'create_custom_item')
                    34. expr
                         L.  49       118  LOAD_CONST               ('^delete_custom_item', 'delete_custom_item')
                    35. expr
                         L.  50       121  LOAD_CONST               ('^modify_custom_item', 'modify_custom_item')
                    36. expr
                         L.  52       124  LOAD_CONST               ('^get_settings', 'get_settings')
                    37. expr
                         L.  53       127  LOAD_CONST               ('^set_settings', 'set_settings')
                    38. expr
                         L.  55       130  LOAD_CONST               ('^search_log$', 'search_log')
                    39. expr
                         L.  57       133  LOAD_CONST               ('^search_mail$', 'search_mail')
                    40. expr
                         L.  58       136  LOAD_CONST               ('^add_mail$', 'add_mail')
                    41. expr
                         L.  59       139  LOAD_CONST               ('^delete_mail$', 'delete_mail')
                    42. expr
                         L.  60       142  LOAD_CONST               ('^get_all_mail$', 'get_all_mail')
                    43. expr
                         L.  63       145  LOAD_CONST               ('^get_report_list$', 'get_report_list')
                    44. expr
                         L.  64       148  LOAD_CONST               ('^delete_report$', 'delete_report')
                    45. expr
                         L.  65       151  LOAD_CONST               ('^get_report_server_by_id$', 'get_report_server_by_id')
                    46. expr
                         L.  66       154  LOAD_CONST               ('^get_job_result_by_api$', 'get_job_result_by_api')
                    47. expr
                         L.  67       157  LOAD_CONST               ('^get_report_error_summary_by_id', 'get_report_error_summary_by_id')
                    48. expr
                         L.  68       160  LOAD_CONST               ('^get_report_server_detail_by_id$', 'get_report_server_detail_by_id')
                    49. expr
                         L.  71       163  LOAD_CONST               ('^export_check_server/$', 'export_check_server')
                    50. expr
                         L.  72       166  LOAD_CONST               ('^export_check_error_summary/$', 'export_check_error_summary')
                    51. expr
                         L.  75       169  LOAD_CONST               ('^upload_img/$', 'upload_img')
                    52. expr
                         L.  76       172  LOAD_CONST               ('^show_logo/$', 'show_logo')
                    53. expr
                         L.  77       175  LOAD_CONST               ('^set_default_img$', 'set_default_img')
                    54.               178  CALL_FUNCTION_53     53  None
             1. store
                              181  STORE_NAME            2  'urlpatterns'

---- end before transform
---- begin after transform
    stmts (2)
     0. import_from (5)
         0.  L.   3         0  LOAD_CONST               -1
         1.                 3  LOAD_CONST               ('patterns',)
         2.                 6  IMPORT_NAME           0  'django.conf.urls'
         3. importlist
            alias (2)
                 0.                 9  IMPORT_FROM           1  'patterns'
                 1. store
                                   12  STORE_NAME            1  'patterns'
         4.                15  POP_TOP          
     1. assign (2)
         0. expr
            call (55)
                 0. expr
                     L.   5        16  LOAD_NAME             1  'patterns'
                 1. expr
                     L.   6        19  LOAD_CONST               'home_application.views'
                 2. expr
                     L.   8        22  LOAD_CONST               ('^$', 'home')
                 3. expr
                     L.   9        25  LOAD_CONST               ('^export_page/', 'export_page')
                 4. expr
                     L.  11        28  LOAD_CONST               ('^get_count_obj$', 'get_count_obj')
                 5. expr
                     L.  12        31  LOAD_CONST               ('^update_url$', 'update_url')
                 6. expr
                     L.  15        34  LOAD_CONST               ('^get_all_business$', 'get_all_business')
                 7. expr
                     L.  16        37  LOAD_CONST               ('^search_business_servers$', 'search_business_servers')
                 8. expr
                     L.  17        40  LOAD_CONST               ('^search_business_topo/$', 'search_business_topo')
                 9. expr
                     L.  18        43  LOAD_CONST               ('^search_module_servers/$', 'search_module_servers')
                10. expr
                     L.  19        46  LOAD_CONST               ('^get_check_servers$', 'get_check_servers')
                11. expr
                     L.  20        49  LOAD_CONST               ('^get_app_check_servers$', 'get_app_check_servers')
                12. expr
                     L.  23        52  LOAD_CONST               ('^get_task_option$', 'get_task_option')
                13. expr
                     L.  24        55  LOAD_CONST               ('^get_user_mail$', 'get_user_mail')
                14. expr
                     L.  25        58  LOAD_CONST               ('^create_task$', 'create_task')
                15. expr
                     L.  26        61  LOAD_CONST               ('^create_check_job_by_api$', 'create_check_job_by_api')
                16. expr
                     L.  27        64  LOAD_CONST               ('^get_task_list$', 'get_task_list')
                17. expr
                     L.  28        67  LOAD_CONST               ('^get_check_task_by_api$', 'get_check_task_by_api')
                18. expr
                     L.  29        70  LOAD_CONST               ('^run_task_now$', 'run_task_now')
                19. expr
                     L.  30        73  LOAD_CONST               ('^modify_task$', 'modify_task')
                20. expr
                     L.  31        76  LOAD_CONST               ('^task_clone$', 'task_clone')
                21. expr
                     L.  32        79  LOAD_CONST               ('^delete_task$', 'delete_task')
                22. expr
                     L.  33        82  LOAD_CONST               ('^search_dynamic_group_list$', 'search_dynamic_group_list')
                23. expr
                     L.  34        85  LOAD_CONST               ('^check_app_topo$', 'check_app_topo')
                24. expr
                     L.  35        88  LOAD_CONST               ('^get_check_topo$', 'get_check_topo')
                25. expr
                     L.  36        91  LOAD_CONST               ('^search_app_topo$', 'search_app_topo')
                26. expr
                     L.  39        94  LOAD_CONST               ('^get_module_item_list$', 'get_module_item_list')
                27. expr
                     L.  40        97  LOAD_CONST               ('^search_module_list$', 'search_module_list')
                28. expr
                     L.  41       100  LOAD_CONST               ('^get_module_list$', 'get_module_list')
                29. expr
                     L.  42       103  LOAD_CONST               ('^create_module$', 'create_module')
                30. expr
                     L.  43       106  LOAD_CONST               ('^modify_module$', 'modify_module')
                31. expr
                     L.  44       109  LOAD_CONST               ('^delete_module$', 'delete_module')
                32. expr
                     L.  47       112  LOAD_CONST               ('^get_item_list', 'get_item_list')
                33. expr
                     L.  48       115  LOAD_CONST               ('^create_custom_item', 'create_custom_item')
                34. expr
                     L.  49       118  LOAD_CONST               ('^delete_custom_item', 'delete_custom_item')
                35. expr
                     L.  50       121  LOAD_CONST               ('^modify_custom_item', 'modify_custom_item')
                36. expr
                     L.  52       124  LOAD_CONST               ('^get_settings', 'get_settings')
                37. expr
                     L.  53       127  LOAD_CONST               ('^set_settings', 'set_settings')
                38. expr
                     L.  55       130  LOAD_CONST               ('^search_log$', 'search_log')
                39. expr
                     L.  57       133  LOAD_CONST               ('^search_mail$', 'search_mail')
                40. expr
                     L.  58       136  LOAD_CONST               ('^add_mail$', 'add_mail')
                41. expr
                     L.  59       139  LOAD_CONST               ('^delete_mail$', 'delete_mail')
                42. expr
                     L.  60       142  LOAD_CONST               ('^get_all_mail$', 'get_all_mail')
                43. expr
                     L.  63       145  LOAD_CONST               ('^get_report_list$', 'get_report_list')
                44. expr
                     L.  64       148  LOAD_CONST               ('^delete_report$', 'delete_report')
                45. expr
                     L.  65       151  LOAD_CONST               ('^get_report_server_by_id$', 'get_report_server_by_id')
                46. expr
                     L.  66       154  LOAD_CONST               ('^get_job_result_by_api$', 'get_job_result_by_api')
                47. expr
                     L.  67       157  LOAD_CONST               ('^get_report_error_summary_by_id', 'get_report_error_summary_by_id')
                48. expr
                     L.  68       160  LOAD_CONST               ('^get_report_server_detail_by_id$', 'get_report_server_detail_by_id')
                49. expr
                     L.  71       163  LOAD_CONST               ('^export_check_server/$', 'export_check_server')
                50. expr
                     L.  72       166  LOAD_CONST               ('^export_check_error_summary/$', 'export_check_error_summary')
                51. expr
                     L.  75       169  LOAD_CONST               ('^upload_img/$', 'upload_img')
                52. expr
                     L.  76       172  LOAD_CONST               ('^show_logo/$', 'show_logo')
                53. expr
                     L.  77       175  LOAD_CONST               ('^set_default_img$', 'set_default_img')
                54.               178  CALL_FUNCTION_53     53  None
         1. store
                          181  STORE_NAME            2  'urlpatterns'

from django.conf.urls import patterns
urlpatterns = patterns('home_application.views', ('^$', 'home'), ('^export_page/',
                                                                  'export_page'), ('^get_count_obj$',
                                                                                   'get_count_obj'), ('^update_url$',
                                                                                                      'update_url'), ('^get_all_business$',
                                                                                                                      'get_all_business'), ('^search_business_servers$',
                                                                                                                                            'search_business_servers'), ('^search_business_topo/$',
                                                                                                                                                                         'search_business_topo'), ('^search_module_servers/$',
                                                                                                                                                                                                   'search_module_servers'), ('^get_check_servers$',
                                                                                                                                                                                                                              'get_check_servers'), ('^get_app_check_servers$',
                                                                                                                                                                                                                                                     'get_app_check_servers'), ('^get_task_option$',
                                                                                                                                                                                                                                                                                'get_task_option'), ('^get_user_mail$',
                                                                                                                                                                                                                                                                                                     'get_user_mail'), ('^create_task$',
                                                                                                                                                                                                                                                                                                                        'create_task'), ('^create_check_job_by_api$',
                                                                                                                                                                                                                                                                                                                                         'create_check_job_by_api'), ('^get_task_list$',
                                                                                                                                                                                                                                                                                                                                                                      'get_task_list'), ('^get_check_task_by_api$',
                                                                                                                                                                                                                                                                                                                                                                                         'get_check_task_by_api'), ('^run_task_now$',
                                                                                                                                                                                                                                                                                                                                                                                                                    'run_task_now'), ('^modify_task$',
                                                                                                                                                                                                                                                                                                                                                                                                                                      'modify_task'), ('^task_clone$',
                                                                                                                                                                                                                                                                                                                                                                                                                                                       'task_clone'), ('^delete_task$',
                                                                                                                                                                                                                                                                                                                                                                                                                                                                       'delete_task'), ('^search_dynamic_group_list$',
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        'search_dynamic_group_list'), ('^check_app_topo$',
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       'check_app_topo'), ('^get_check_topo$',
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           'get_check_topo'), ('^search_app_topo$',
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               'search_app_topo'), ('^get_module_item_list$',
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    'get_module_item_list'), ('^search_module_list$',
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              'search_module_list'), ('^get_module_list$',
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      'get_module_list'), ('^create_module$',
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           'create_module'), ('^modify_module$',
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              'modify_module'), ('^delete_module$',
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 'delete_module'), ('^get_item_list',
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    'get_item_list'), ('^create_custom_item',
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       'create_custom_item'), ('^delete_custom_item',
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               'delete_custom_item'), ('^modify_custom_item',
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       'modify_custom_item'), ('^get_settings',
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               'get_settings'), ('^set_settings',
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 'set_settings'), ('^search_log$',
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   'search_log'), ('^search_mail$',
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   'search_mail'), ('^add_mail$',
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    'add_mail'), ('^delete_mail$',
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  'delete_mail'), ('^get_all_mail$',
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   'get_all_mail'), ('^get_report_list$',
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     'get_report_list'), ('^delete_report$',
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          'delete_report'), ('^get_report_server_by_id$',
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             'get_report_server_by_id'), ('^get_job_result_by_api$',
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          'get_job_result_by_api'), ('^get_report_error_summary_by_id',
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     'get_report_error_summary_by_id'), ('^get_report_server_detail_by_id$',
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         'get_report_server_detail_by_id'), ('^export_check_server/$',
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             'export_check_server'), ('^export_check_error_summary/$',
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      'export_check_error_summary'), ('^upload_img/$',
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      'upload_img'), ('^show_logo/$',
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      'show_logo'), ('^set_default_img$',
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     'set_default_img'))
# okay decompiling urls.pyc
