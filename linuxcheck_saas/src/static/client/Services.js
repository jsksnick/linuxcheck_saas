services = angular.module('webApiService', ['ngResource', 'utilServices']);

//生产代码
var POST = "POST";
var GET = "GET";

//测试代码
//var sourceRoute = "./Client/MockData";
//var fileType = ".html";
//var POST = "GET";
//var GET = "GET";
services.factory('sysService', ['$resource', function ($resource) {
    return $resource(site_url + ':actionName/', {},
        {
            search_log: {method: POST, params: {actionName: 'search_log'}, isArray: false},
            search_mail: {method: POST, params: {actionName: 'search_mail'}, isArray: false},
            add_mail: {method: POST, params: {actionName: 'add_mail'}, isArray: false},
            modify_mail: {method: POST, params: {actionName: 'modify_mail'}, isArray: false},
            delete_mail: {method: POST, params: {actionName: 'delete_mail'}, isArray: false},
            get_count_obj: {method: POST, params: {actionName: 'get_count_obj'}, isArray: false},
            update_url: {method: POST, params: {actionName: 'update_url'}, isArray: false},
            get_settings: {method: POST, params: {actionName: 'get_settings'}, isArray: false},
            set_settings: {method: POST, params: {actionName: 'set_settings'}, isArray: false},
            search_app_list: {method: POST, params: {actionName: 'search_app_list'}, isArray: false},
            delete_app: {method: POST, params: {actionName: 'delete_app'}, isArray: false},
            sync_app: {method: POST, params: {actionName: 'sync_app'}, isArray: false},
            get_user_app_list: {method: POST, params: {actionName: 'get_user_app_list'}, isArray: false},
            add_app: {method: POST, params: {actionName: 'add_app'}, isArray: false},
            search_business_servers: {method: POST, params: {actionName: 'search_business_servers'}, isArray: false},
            search_business_topo: {method: POST, params: {actionName: 'search_business_topo'}, isArray: false},
            search_module_servers: {method: GET, params: {actionName: 'search_module_servers'}, isArray: false},
            get_check_servers: {method: POST, params: {actionName: 'get_check_servers'}, isArray: false},
            get_all_mail: {method: POST, params: {actionName: 'get_all_mail'}, isArray: false},
            set_default_img: {method: POST, params: {actionName: 'set_default_img'}, isArray: false},
            get_all_business: {method: POST, params: {actionName: 'get_all_business'}, isArray: false},
            get_app_check_servers: {method: POST, params: {actionName: 'get_app_check_servers'}, isArray: false},
        });
}])

    .factory('taskService', ['$resource', function ($resource) {
        return $resource(site_url + ':actionName/', {}, {
            get_task_list: {method: POST, params: {actionName: 'get_task_list'}, isArray: false},
            get_task_info: {method: POST, params: {actionName: 'get_task_info'}, isArray: false},
            get_task_option: {method: POST, params: {actionName: 'get_task_option'}, isArray: false},
            get_user_mail: {method: POST, params: {actionName: 'get_user_mail'}, isArray: false},
            create_task: {method: POST, params: {actionName: 'create_task'}, isArray: false},
            delete_task: {method: POST, params: {actionName: 'delete_task'}, isArray: false},
            modify_task: {method: POST, params: {actionName: 'modify_task'}, isArray: false},
            task_clone: {method: POST, params: {actionName: 'task_clone'}, isArray: false},
            run_task_now: {method: POST, params: {actionName: 'run_task_now'}, isArray: false},
            get_task_obj: {method: POST, params: {actionName: 'get_task_obj'}, isArray: false},

            get_item_list: {method: POST, params: {actionName: 'get_item_list'}, isArray: false},
            create_custom_item: {method: POST, params: {actionName: 'create_custom_item'}, isArray: false},
            delete_custom_item: {method: POST, params: {actionName: 'delete_custom_item'}, isArray: false},
            modify_custom_item: {method: POST, params: {actionName: 'modify_custom_item'}, isArray: false},
            search_dynamic_group_list: {method: POST, params: {actionName: 'search_dynamic_group_list'}, isArray: false},
            get_all_business: {method: POST, params: {actionName: 'get_all_business'}, isArray: false},
            get_check_topo: {method: POST, params: {actionName: 'get_check_topo'}, isArray: false},
            check_app_topo: {method: POST, params: {actionName: 'check_app_topo'}, isArray: false},
        });
    }])
    .factory('moduleService', ['$resource', function ($resource) {
        return $resource(site_url + ':actionName/', {}, {
            get_module_list: {method: POST, params: {actionName: 'get_module_list'}, isArray: false},
            get_module_item_list: {method: POST, params: {actionName: 'get_module_item_list'}, isArray: false},
            create_module: {method: POST, params: {actionName: 'create_module'}, isArray: false},
            modify_module: {method: POST, params: {actionName: 'modify_module'}, isArray: false},
            delete_module: {method: POST, params: {actionName: 'delete_module'}, isArray: false},
            search_module_list: {method: POST, params: {actionName: 'search_module_list'}, isArray: false},
        });
    }])
    .factory('reportService', ['$resource', function ($resource) {
        return $resource(site_url + ':actionName/', {}, {
            get_report_list: {method: POST, params: {actionName: 'get_report_list'}, isArray: false},
            delete_report: {method: POST, params: {actionName: 'delete_report'}, isArray: false},
            get_server_detail: {method: POST, params: {actionName: 'get_server_detail'}, isArray: false},
            get_report_server_by_id: {method: POST, params: {actionName: 'get_report_server_by_id'}, isArray: false},
            get_report_error_summary_by_id: {method: GET, params: {actionName: 'get_report_error_summary_by_id'}, isArray: false},
            get_report_server_detail_by_id: {method: POST, params: {actionName: 'get_report_server_detail_by_id'}, isArray: false},
            export_check_server: {method: POST, params: {actionName: 'export_check_server'}, isArray: false}
        });
    }])
;//这是结束符，请勿删除