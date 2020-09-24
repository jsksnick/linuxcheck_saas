controllers.controller("taskListCtrl", ["$scope", "errorModal", "msgModal", "$modal", "loading", "confirmModal", "taskService", function ($scope, errorModal, msgModal, $modal, loading, confirmModal, taskService) {
    $scope.args = {
        task_name: "",
        task_type: "00"
    };
    $scope.taskList = [];
    $scope.PagingData = [];
    $scope.totalSerItems = 0;

    $scope.pagingOptions = {
        pageSizes: [10, 50, 100],
        pageSize: "10",
        currentPage: 1
    };

    $scope.showTask = false;
    $scope.searchList = function () {
        loading.open();
        taskService.get_task_list({}, $scope.args, function (res) {
            loading.close();
            if (res.result) {
                $scope.taskList = res.data;
                $scope.pagingOptions.currentPage = 1;
                $scope.getPagedDataAsync($scope.pagingOptions.pageSize, $scope.pagingOptions.currentPage);
            }
            else {
                errorModal.open(res.data);
            }
        })
    };

    $scope.getPagedDataAsync = function (pageSize, page) {
        $scope.setPagingData($scope.taskList ? $scope.taskList : [], pageSize, page);
    };
    $scope.setPagingData = function (data, pageSize, page) {
        $scope.PagingData = data.slice((page - 1) * pageSize, page * pageSize);
        $scope.totalSerItems = data.length;
        if (!$scope.$$phase) {
            $scope.$apply();
        }
    };

    $scope.$watch('pagingOptions', function (newVal, oldVal) {
        $scope.getPagedDataAsync($scope.pagingOptions.pageSize, $scope.pagingOptions.currentPage);
    }, true);

    $scope.searchList();
    $scope.gridOption = {
        data: "PagingData",
        enablePaging: true,
        showFooter: true,
        pagingOptions: $scope.pagingOptions,
        totalServerItems: 'totalSerItems',
        columnDefs: [
            {field: "name", displayName: "任务名", width: 200},
            {displayName: "巡检对象",cellTemplate:'' +
                '<div style="line-height: 30px;padding-left: 5px;vertical-align: middle;width:100%;text-overflow: ellipsis;overflow: hidden;white-space: nowrap">' +
                '<span ng-if="row.entity.select_type==\'ip\'" ng-repeat="i in row.entity.servers" title="{{i.ip}}({{i.source}})">{{i.ip}}({{i.source}});</span>' +
                '<span ng-if="row.entity.select_type==\'group\'" ng-repeat="i in row.entity.groups" title="{{i.group_name}}({{i.app_name}})">{{i.group_name}}({{i.app_name}});</span>' +
                '<span ng-if="row.entity.select_type==\'topo\'" ng-repeat="i in row.entity.topos" title="{{i.node_name}}">{{i.node_name}};</span></div>'},
            {field: "check_module.name", displayName: "巡检模板", width: 100},
            {field: "type_name", displayName: "任务类型", width: 100},
            {field: "when_created", displayName: "创建时间", width: 150},
            {
                displayName: "操作", width: 200,
                cellTemplate: '<div style="padding-top:5px;text-align: center;">' +
                '<span class="label label-sm label-success label-btn button-radius" ng-click="runTask(row.entity)">立即执行</span>&nbsp;' +
                // '<span class="label label-sm label-info label-btn button-radius" ng-click="modifyTask(row.entity)">修改</span>&nbsp;' +
                '<span class="label label-sm label-info label-btn button-radius" ng-click="cloneTask(row.entity)">克隆</span>&nbsp;' +
                '<span class="label label-sm label-danger label-btn button-radius" ng-click="deleteTask(row)">删除</span>' +
                '</div>'
            }
        ]
    };

    $scope.deleteTask = function (row) {
        confirmModal.open({
            text: "是否要删除该任务",
            confirmClick: function () {
                loading.open();
                taskService.delete_task({}, row.entity, function (res) {
                    loading.close();
                    if (res.result) {
                        msgModal.open("success", "删除成功");
                        $scope.searchList();
                    }
                    else {
                        errorModal.open([res.data]);
                    }
                })
            }
        })
    };

    $scope.runTask = function (rowEntity) {
        confirmModal.open({
            text: "是否要立即执行该任务",
            confirmClick: function () {
                loading.open();
                taskService.run_task_now({task_id: rowEntity.id}, {}, function (res) {
                    loading.close();
                    if (res.result) {
                        msgModal.open("success", "启动成功");
                        window.location.href = "#/reportHistory";
                    }
                    else {
                        errorModal.open([res.data]);
                    }
                })
            }
        })
    };

    $scope.modifyTask = function (rowEntity) {
        var modalInstance = $modal.open({
            templateUrl: static_url + 'client/views/taskManagement/taskModify.html',
            windowClass: 'task_dialog',
            controller: 'taskModifyCtrl',
            backdrop: 'static',
            resolve: {
                itemObj: function () {
                    return angular.copy(rowEntity);
                }
            }
        });
        modalInstance.result.then(function () {
            $scope.searchList();
        })
    };
    $scope.cloneTask = function (rowEntity) {
        var modalInstance = $modal.open({
            templateUrl: static_url + 'client/views/taskManagement/taskClone.html',
            windowClass: 'task_dialog',
            controller: 'taskCloneCtrl',
            backdrop: 'static',
            resolve: {
                itemObj: function () {
                    return angular.copy(rowEntity);
                }
            }
        });
        modalInstance.result.then(function () {
            $scope.searchList();
        })
    };
}]);



