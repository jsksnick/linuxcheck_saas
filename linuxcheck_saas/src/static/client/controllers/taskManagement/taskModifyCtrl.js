controllers.controller("taskModifyCtrl", function ($scope, $filter, errorModal, itemObj, msgModal, taskService, sysService, $modalInstance, loading, $modal) {
    $scope.args = itemObj;
    if (itemObj.time_type === "time") {
        $scope.args.runTime = itemObj.first_time;
        $scope.args.cycleTime = "";
        $scope.args.interval = "";
    }
    else if (itemObj.time_type === "cycle") {
        $scope.args.cycleTime = itemObj.first_time;
        $scope.args.interval = itemObj.time_interval;
        $scope.args.runTime = "";

    }

    $scope.serverList = [];
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
        taskService.modify_task({}, $scope.args, function (res) {
            loading.close();
            if (res.result) {
                msgModal.open("success", "修改成功");
                // if ($scope.args.time_type === "now") {
                //     window.location.href = "#/reportHistory";
                // }
                $modalInstance.close();
            }
            else {
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
        if ($scope.args.servers.length === 0) {
            errors.push("巡检服务器不能为空！");
        }
        if ($scope.args.script_account === "") {
            errors.push("执行帐户不能为空！");
        }
        if ($scope.args.time_type === "time") {
            var one_errors1 = CWApp.ValidateDate($filter, $scope.args.runTime);
            if (one_errors1 !== "") {
                errors.push(one_errors1)
            }
        }
        else if ($scope.args.time_type === "cycle") {
            var one_errors2 = CWApp.ValidateDate($filter, $scope.args.cycleTime);
            if (one_errors2 !== "") {
                errors.push(one_errors2)
            }
            if ($scope.args.interval < 1) {
                errors.push("时间间隔必须为大于0的整数");
            }
        }
        return errors;
    };

    $scope.cancel = function () {
        $modalInstance.dismiss("cancel");
    };

    $scope.select_server = function () {
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
            $scope.args.servers = [];
            var tmp = [];
            for (var i = 0; i < servers.length; i++) {
                tmp.push({ip: servers[i].ip, source: servers[i].source, app_id: servers[i].app_id, server_name: servers[i].bk_os_name,source_name:servers[i].source_name});
            }
            $scope.args.servers = tmp;
        });
    };

    $scope.gridOption = {
        data: 'args.servers',
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

    $scope.deleteServer = function (row) {
        $scope.args.servers.splice($scope.args.servers.indexOf(row.entity), 1);
    };

});