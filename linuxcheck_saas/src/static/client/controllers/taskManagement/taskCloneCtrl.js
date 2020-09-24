controllers.controller("taskCloneCtrl", function ($scope, $filter, errorModal, itemObj, msgModal, taskService, sysService, $modalInstance, loading, $modal) {
    $scope.args = itemObj;

    // 巡检对象初始化
    $scope.serverSelect = $scope.args.servers;
    $scope.oldData = angular.copy($scope.args.servers);
    $scope.groupSelect = $scope.args.groups;
    $scope.oldGroupData = angular.copy($scope.args.groups);
    $scope.topoSelect = $scope.args.topos;
    $scope.oldTopoData = angular.copy($scope.args.topos);

    $scope.search = {
        search_ip: '',
        search_node: '',
        search_group: ''
    };
    $scope.today = new Date();
    $scope.timeString = $filter('date')($scope.today, 'yyyyMMddHHmmss');
    $scope.args.name = $scope.args.name + "clone" + $scope.timeString;

    if (itemObj.time_type === "time") {
        $scope.args.runTime = itemObj.first_time;
        $scope.args.cycleTime = "";
        $scope.args.interval = "";
    } else if (itemObj.time_type === "cycle") {
        $scope.args.cycleTime = itemObj.first_time;
        $scope.args.interval = itemObj.time_interval;
        $scope.args.runTime = "";

    }

    $scope.moduleList = [];
    $scope.mailList = [];

    $scope.moduleOption = {
        data: "moduleList",
        modelData: "args.check_module_id",
        multiple: false
    };

    $scope.receiverOpt = {
        data: "mailList",
        modelData: "args.receivers",
        multiple: true
    };

    $scope.init = function () {
        loading.open();
        taskService.get_task_option({}, {type_id: $scope.args.check_module.os_type}, function (res) {
            loading.close();
            if (res.result) {
                $scope.mailList = res.mail_list;
                $scope.moduleList = res.module_list;
            }
        });
    };
    $scope.init();

    $scope.confirm = function () {
        var errors = validateObj();
        if (errors.length > 0) {
            errorModal.open(errors);
            return;
        }
        loading.open();
        var obj = angular.copy($scope.args);
        obj.servers = angular.copy($scope.serverSelect);
        obj.groups =  angular.copy($scope.groupSelect);
        obj.nodes =  angular.copy($scope.topoSelect);
        taskService.task_clone({}, obj, function (res) {
            loading.close();
            if (res.result) {
                msgModal.open("success", "克隆成功");
                // if ($scope.args.time_type === "now") {
                //     window.location.href = "#/reportHistory";
                // }
                $modalInstance.close();
            } else {
                errorModal.open(res.data);
            }
        })
    };

    var validateObj = function () {
        var errors = [];
        if ($scope.args.name === "") {
            errors.push("任务名称不能为空！");
        }
        if ($scope.args.check_module_id === "") {
            errors.push("巡检模板不能为空！");
        }
        if ($scope.args.script_account === "") {
            errors.push("执行帐户不能为空！");
        }
        if ($scope.args.time_type === "time") {
            var one_errors1 = CWApp.ValidateDate($filter, $scope.args.runTime);
            if (one_errors1 !== "") {
                errors.push(one_errors1)
            }
        } else if ($scope.args.time_type === "cycle") {
            var one_errors2 = CWApp.ValidateDate($filter, $scope.args.cycleTime);
            if (one_errors2 !== "") {
                errors.push(one_errors2)
            }
            if ($scope.args.interval < 1) {
                errors.push("时间间隔必须为大于0的整数！");
            }
        }
        if($scope.args.select_type == ""){
            errors.push("请选择巡检对象！");
        }
        else if ($scope.args.select_type == "ip" && $scope.serverSelect.length === 0){
            errors.push("请选择巡检对象！");
        }
        else if ($scope.args.select_type == "group" && $scope.groupSelect.length === 0){
            errors.push("请选择巡检对象！");
        }
        else if ($scope.args.select_type == "topo" && $scope.topoSelect.length === 0){
            errors.push("请选择巡检对象！");
        }
        return errors;
    };

    $scope.cancel = function () {
        $modalInstance.dismiss("cancel");
    };

    $scope.select_server = function () {
        var exitList = [];
        if ($scope.oldData.length > 0) {
            angular.forEach($scope.oldData, function (item) {
                exitList.push(item.ip + '@' + item.source);
            });
        }
        var modalInstance = $modal.open({
            templateUrl: static_url + 'client/views/taskManagement/selectServers.html',
            windowClass: 'serverDialog',
            controller: 'selectServersCtrl',
            backdrop: 'static',
            resolve: {
                itemObj: function () {
                    return $scope.args.check_module.os_type;
                }
            }
        });
        modalInstance.result.then(function (servers) {
            $scope.args.search_ip = '';
            $scope.args.select_type = 'ip';
            for (var i = 0; i < servers.length; i++) {
                if (exitList.indexOf(servers[i].ip + '@' + servers[i].source) === -1) {
                    $scope.serverSelect.push({
                        'ip': servers[i].ip,
                        'source': servers[i].source,
                        'app_id': servers[i].app_id,
                        'server_name': servers[i].bk_os_name,
                        'source_name': servers[i].source_name
                    });
                }
            }
            $scope.oldData = angular.copy($scope.serverSelect);
            // 其他数据置空
            $scope.groupSelect = [];
            $scope.oldGroupData = [];
            $scope.topoSelect = [];
            $scope.oldTopoData = [];
        });
    };

    $scope.deleteServer = function (row) {
        loading.open();
        var deleteCharge = row.entity.ip + '@' + row.entity.source;
        $scope.serverSelect.splice($scope.serverSelect.indexOf(row.entity), 1);
        for (var i = 0; i < $scope.oldData.length; i++) {
            var charge = $scope.oldData[i].ip + '@' + $scope.oldData[i].source;
            if (charge === deleteCharge) {
                $scope.oldData.splice(i, 1);
                if ($scope.serverSelect.length === 0) {
                    $scope.serverSelect = angular.copy($scope.oldData);
                }
                loading.close();
                return;
            }
        }
    };

     $scope.searchIp = function () {
        if ($scope.args.search_ip === '') {
            $scope.serverSelect = angular.copy($scope.oldData);
        } else {
            var searchData = [];
            $scope.serverSelect = angular.copy($scope.oldData);
            angular.forEach($scope.serverSelect, function (item) {
                if (item.ip.indexOf($scope.args.search_ip) > -1) {
                    searchData.push(item);
                }
            });
            $scope.serverSelect = searchData;
        }
    };

    $scope.gridOption = {
        data: 'serverSelect',
        enableSorting: false,
        columnDefs: [
            {field: 'source_name', displayName: '区域名称', width: 100},
            {field: 'ip', displayName: 'IP地址', width: 120},
            {field: 'server_name', displayName: '操作系统'},

            {
                displayName: '操作', width: 60, height: 0,
                cellTemplate: '<div style="width:100%;text-align: center;padding-top: 5px;z-index: 1">' +
                    '<span ng-click="deleteServer(row)" class="label label-danger button-radius" style="min-width:50px;margin-left: 5px;cursor:pointer;">删除</span>' +
                    '</div>'
            }
        ]
    };

    // 动态分组
    $scope.select_group = function () {
        var exitGroup = [];
        angular.forEach($scope.oldGroupData, function (obj) {
            exitGroup.push(obj.group_id);
        });
        var modalInstance = $modal.open({
            templateUrl: static_url + 'client/views/taskManagement/selectGroups.html',
            windowClass: 'serverDialog',
            controller: 'selectGroupsCtrl',
            backdrop: 'static'
        });
        modalInstance.result.then(function (groups) {
            //其他数据置空
            $scope.args.select_type = "group";
            $scope.serverSelect = [];
            $scope.oldData = [];
            $scope.topoSelect = [];
            $scope.oldTopoData = [];
            angular.forEach(groups, function (obj) {
                if(exitGroup.indexOf(obj.group_id) < 0){
                    $scope.groupSelect.push({
                        app_id: obj.app_id,
                        app_name: obj.app_name,
                        group_id: obj.group_id,
                        group_name: obj.group_name,
                        create_user: obj.create_user,
                        type: 'group'
                    });
                }
            });
            $scope.oldGroupData = angular.copy($scope.groupSelect);

        });
    };

    $scope.gridGroup = {
        data: 'groupSelect',
        enableSorting: false,
        columnDefs: [
            {field: 'app_name', displayName: '业务名称'},
            {field: 'group_name', displayName: '分组名称'},
            {
                displayName: '操作', width: 60, height: 0,
                cellTemplate: '<div style="width:100%;text-align: center;padding-top: 5px;z-index: 1">' +
                    '<span ng-click="deleteGroup(row.entity)" class="label label-danger" style="min-width:50px;margin-left: 5px;cursor:pointer;">删除</span>' +
                    '</div>'
            }
        ]
    };

    $scope.deleteGroup = function (rowEntity) {
        loading.open();
        $scope.groupSelect.splice($scope.groupSelect.indexOf(rowEntity), 1);
        for(var i=0; i < $scope.oldGroupData.length; i++){
            if($scope.oldGroupData[i].group_id == rowEntity.group_id){
                $scope.oldGroupData.splice(i,1);
                loading.close();
                break;
            }
        }
        $scope.groupSelect = angular.copy($scope.oldGroupData);
        if($scope.groupSelect.length === 0){
            $scope.args.search_group = "";
        }
    };

    $scope.searchGroup = function () {
        if ($scope.args.search_group === '') {
            $scope.groupSelect = angular.copy($scope.oldGroupData);
        } else {
            var searchData = [];
             $scope.groupSelect = angular.copy($scope.oldGroupData);
            angular.forEach($scope.groupSelect, function (item) {
                if (item.group_name.toUpperCase().indexOf($scope.args.search_group.toUpperCase()) > -1) {
                    searchData.push(item);
                }
            });
            $scope.groupSelect = searchData;
        }
    };

    // 业务拓扑选择
    $scope.select_topo = function () {
        var exitTopo = [];
        angular.forEach($scope.oldTopoData, function (obj) {
            exitTopo.push(obj.node_name);
        });
        var modalInstance = $modal.open({
            templateUrl: static_url + 'client/views/taskManagement/selectTopo.html',
            windowClass: 'serverDialog',
            controller: 'selectTopoCtrl',
            backdrop: 'static'
        });
        modalInstance.result.then(function (nodes) {
            $scope.args.select_type = "topo";
            angular.forEach(nodes, function (obj) {
                if(exitTopo.indexOf(obj.node_name) < 0){
                    $scope.topoSelect.push(obj);
                }
            });
            $scope.oldTopoData = angular.copy($scope.topoSelect);

            //其他数据置空
            $scope.serverSelect = [];
            $scope.oldData = [];
            $scope.groupSelect = [];
            $scope.oldGroupData = [];
        });
    };

     $scope.gridTopo = {
        data: 'topoSelect',
        enableSorting: false,
        columnDefs: [
            {field: 'bk_biz_name', displayName: '业务名称'},
            {field: 'node_name', displayName: '节点名称'},
            {field: 'bk_obj_name', displayName: '节点类型'},
            {
                displayName: '操作', width: 60, height: 0,
                cellTemplate: '<div style="width:100%;text-align: center;padding-top: 5px;z-index: 1">' +
                    '<span ng-click="deleteNode(row.entity)" class="label label-danger" style="min-width:50px;margin-left: 5px;cursor:pointer;">删除</span>' +
                    '</div>'
            }
        ]
    };

     $scope.deleteNode = function (rowEntity) {
        loading.open();
        $scope.topoSelect.splice($scope.topoSelect.indexOf(rowEntity), 1);
        for(var i=0; i < $scope.oldTopoData.length; i++){
            if($scope.oldTopoData[i].node_name == rowEntity.node_name){
                $scope.oldTopoData.splice(i,1);
                loading.close();
                break;
            }
        }
        $scope.topoSelect = angular.copy($scope.oldTopoData);
        if($scope.topoSelect.length === 0){
            $scope.args.search_node = "";
        }
    };

     $scope.searchNode = function () {
        if ($scope.args.search_node === '') {
            $scope.topoSelect = angular.copy($scope.oldTopoData);
        } else {
            var searchData = [];
            $scope.topoSelect = angular.copy($scope.oldTopoData);
            angular.forEach($scope.topoSelect, function (item) {
                if (item.node_name.toUpperCase().indexOf($scope.args.search_node.toUpperCase()) > -1) {
                    searchData.push(item);
                }
            });
            $scope.topoSelect = searchData;
        }
    };

    // $scope.select_server = function () {
    //     var exitList = [];
    //     if ($scope.oldData.length > 0) {
    //         angular.forEach($scope.oldData, function (item) {
    //             exitList.push(item.ip + '@' + item.source);
    //         });
    //     }
    //     var modalInstance = $modal.open({
    //         templateUrl: static_url + 'client/views/taskManagement/selectServers.html',
    //         windowClass: 'serverDialog',
    //         controller: 'selectServersCtrl',
    //         backdrop: 'static',
    //         resolve: {
    //             itemObj: function () {
    //                 return $scope.args.check_module.os_type;
    //             }
    //         }
    //     });
    //     modalInstance.result.then(function (servers) {
    //         $scope.search.search_ip = '';
    //         for (var i = 0; i < servers.length; i++) {
    //             if (exitList.indexOf(servers[i].ip + '@' + servers[i].source) === -1) {
    //                 $scope.oldData.push({
    //                     ip: servers[i].ip,
    //                     source: servers[i].source,
    //                     app_id: servers[i].app_id,
    //                     server_name: servers[i].bk_os_name,
    //                     source_name: servers[i].source_name
    //                 });
    //             }
    //         }
    //         $scope.args.servers = angular.copy($scope.oldData);
    //     });
    // };
    //
    // $scope.gridOption = {
    //     data: 'args.servers',
    //     enableSorting: false,
    //     columnDefs: [
    //         {field: 'source_name', displayName: '区域名称', width: 100},
    //         {field: 'ip', displayName: 'IP地址', width: 120},
    //         {field: 'server_name', displayName: '操作系统'},
    //
    //         {
    //             displayName: '操作', width: 60, height: 0,
    //             cellTemplate: '<div style="width:100%;text-align: center;padding-top: 5px;z-index: 1">' +
    //                 '<span ng-click="deleteServer(row)" class="label label-danger button-radius" style="min-width:50px;margin-left: 5px;cursor:pointer;">删除</span>' +
    //                 '</div>'
    //         }
    //     ]
    // };
    //
    // $scope.deleteServer = function (row) {
    //     loading.open();
    //     var deleteCharge = row.entity.ip + '@' + row.entity.source;
    //     $scope.args.servers.splice($scope.args.servers.indexOf(row.entity), 1);
    //     for (var i = 0; i < $scope.oldData.length; i++) {
    //         var charge = $scope.oldData[i].ip + '@' + $scope.oldData[i].source;
    //         if (charge === deleteCharge) {
    //             $scope.oldData.splice(i, 1);
    //             if ($scope.args.servers.length === 0) {
    //                 $scope.args.servers = angular.copy($scope.oldData);
    //             }
    //             loading.close();
    //             return;
    //         }
    //     }
    // };
    //
    // $scope.searchIp = function () {
    //     if ($scope.search.search_ip === '') {
    //         $scope.args.servers = angular.copy($scope.oldData);
    //     } else {
    //         var searchData = [];
    //         angular.forEach($scope.args.servers, function (item) {
    //             if (item.ip.indexOf($scope.search.search_ip) > -1) {
    //                 searchData.push(item);
    //             }
    //         });
    //         $scope.args.servers = searchData;
    //     }
    // };
});