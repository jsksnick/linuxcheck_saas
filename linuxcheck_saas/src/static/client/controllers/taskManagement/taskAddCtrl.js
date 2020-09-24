controllers.controller("taskAddCtrl", function ($scope, $filter, msgModal, taskService, $modal, loading, errorModal) {
    $scope.args = {
        name: "",
        check_module_id: "",
        receivers: "",
        servers: [],
        script_account: "",
        time_type: "now",
        cycleTime: "",
        runTime: "",
        interval: "",
        os_type: "",
        search_ip: '',
        search_group: '',
        search_node: '',
        select_type: ''
    };

    $scope.moduleList = [];
    $scope.mailList = [];

    $scope.osTypeList = [
        {id: 1, text: "CentOS、Redhat系统"},
        {id: 2, text: "SUSE系统"}
    ];
    $scope.osTypeOption = {
        data: "osTypeList",
        modelData: "moduleObj.os_type"
    };

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
        taskService.get_user_mail({}, {}, function (res) {
            if (res.result) {
                $scope.mailList = res.data;
            }
        })
    };
    $scope.init();

    $scope.changeType = function () {
        $scope.moduleList = [];
        loading.open();
        taskService.get_task_option({}, {type_id: $scope.args.os_type}, function (res) {
            loading.close();
            if (res.result) {
                // $scope.mailList = res.mail_list;
                $scope.moduleList = res.module_list;
            } else {
                errorModal.open(res.data);
            }
        });
    };

    $scope.confirm = function () {
        var errors = validateObj();
        if (errors.length > 0) {
            errorModal.open(errors);
            return;
        }
        var taskInfo = {
            name: $scope.args.name,
            check_module_id: $scope.args.check_module_id,
            receivers: $scope.args.receivers,
            select_type: $scope.args.select_type,
            servers: $scope.serverSelect,
            groups: $scope.groupSelect,
            nodes: $scope.topoSelect,
            script_account: $scope.args.script_account,
            time_type: $scope.args.time_type,
            cycleTime: $scope.args.cycleTime,
            runTime: $scope.args.runTime,
            interval: $scope.args.interval,
            os_type: $scope.args.os_type
        };
        loading.open();
        taskService.create_task({}, taskInfo, function (res) {
            loading.close();
            if (res.result) {
                msgModal.open("success", "创建成功");
                if ($scope.args.time_type === "now") {
                    window.location.href = "#/reportHistory";
                } else {
                    window.location.href = "#/taskList";
                }
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
        if ($scope.args.os_type === "") {
            errors.push("系统类型不能为空！")
        }
        if ($scope.args.check_module_id === "") {
            errors.push("巡检模板不能为空！");
        }
        if ($scope.args.script_account === "") {
            errors.push("执行帐户不能为空！");
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
        if ($scope.args.time_type === "time") {
            var one_errors = CWApp.ValidateDate($filter, $scope.args.runTime);
            if (one_errors !== "") {
                errors.push(one_errors)
            }
        } else if ($scope.args.time_type === "cycle") {
            var two_errors = CWApp.ValidateDate($filter, $scope.args.cycleTime);
            if (two_errors !== "") {
                errors.push(two_errors)
            }
            if ($scope.args.interval < 1) {
                errors.push("时间间隔必须为大于0的整数");
            }
        }
        return errors;
    };

    $scope.serverSelect = [];
    $scope.oldData = [];
    $scope.select_server = function () {
        if ($scope.args.os_type === "") {
            errorModal.open(["请先选择系统类型！"]);
            return
        }
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
                    return $scope.args.os_type;
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
    $scope.groupSelect = [];
    $scope.oldGroupData = [];
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
    $scope.topoSelect = [];
    $scope.oldTopoData = [];
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

});