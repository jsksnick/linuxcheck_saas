controllers.controller("customItemCtrl", function ($scope, $modal, loading, errorModal, taskService, msgModal,confirmModal) {
    $scope.filterObj = {
        name: "",
        os_type: ""
    };

    $scope.Pagingdata = [];
    $scope.totalSerItems = 0;

    $scope.pagingOptions = {
        pageSizes: [10, 50, 100],
        pageSize: "10",
        currentPage: 1
    };
    $scope.itemList = [];
    $scope.searchObj = function () {
        taskService.get_item_list({},$scope.filterObj, function (res) {
            if (res.result) {
                $scope.itemList = res.data;
                $scope.pagingOptions.currentPage = 1;
                $scope.getPagedDataAsync($scope.pagingOptions.pageSize, $scope.pagingOptions.currentPage);

            }
            else {
                errorModal.open(res.data);
            }
        })
    };

    $scope.getPagedDataAsync = function (pageSize, page) {
        $scope.setPagingData($scope.itemList ? $scope.itemList : [], pageSize, page);
    };

    $scope.setPagingData = function (data, pageSize, page) {
        $scope.Pagingdata = data.slice((page - 1) * pageSize, page * pageSize);
        $scope.totalSerItems = data.length;
        if (!$scope.$$phase) {
            $scope.$apply();
        }
    };

    $scope.$watch('pagingOptions', function (newVal, oldVal) {
        $scope.getPagedDataAsync($scope.pagingOptions.pageSize, $scope.pagingOptions.currentPage);
    }, true);
    $scope.searchObj();

    $scope.addItem = function () {
        var modalInstance = $modal.open({
            templateUrl: static_url + 'client/views/taskManagement/customItemAdd.html',
            windowClass: 'dialog_custom_item',
            controller: 'customItemAddCtrl',
            backdrop: 'static'
        });
        modalInstance.result.then(function () {
            $scope.searchObj();
        })
    };

    $scope.gridOption = {
        data: "Pagingdata",
        enablePaging: true,
        showFooter: true,
        pagingOptions: $scope.pagingOptions,
        totalServerItems: 'totalSerItems',
        columnDefs: [
            {
                displayName: '系统类型', width: 150,
                cellTemplate: '<div style="line-height: 30px;padding-left: 10px;vertical-align: middle;width:100%;text-overflow: ellipsis;overflow: hidden;white-space: nowrap"><span title="{{row.entity.os_name}}">{{row.entity.os_name}}</span></div>'
            },
            {
                displayName: '巡检字段', width: 150,
                cellTemplate: '<div style="line-height: 30px;padding-left: 10px;vertical-align: middle;width:100%;text-overflow: ellipsis;overflow: hidden;white-space: nowrap"><span title="{{row.entity.name}}">{{row.entity.name}}</span></div>'
            },
            {
                displayName: '巡检项名称', width: 150,
                cellTemplate: '<div style="line-height: 30px;padding-left: 10px;vertical-align: middle;width:100%;text-overflow: ellipsis;overflow: hidden;white-space: nowrap"><span title="{{row.entity.cn_name}}">{{row.entity.cn_name}}</span></div>'
            },
            {
                displayName: '对比方式', width: 100,
                cellTemplate: '<div style="line-height: 30px;padding-left: 10px;vertical-align: middle;width:100%;text-overflow: ellipsis;overflow: hidden;white-space: nowrap"><span title="{{row.entity.compare_way}}">{{row.entity.compare_way}}</span></div>'
            },
            {
                displayName: '对比值', width: 100,
                cellTemplate: '<div style="line-height: 30px;padding-left: 10px;vertical-align: middle;width:100%;text-overflow: ellipsis;overflow: hidden;white-space: nowrap"><span title="{{row.entity.compare_value}}">{{row.entity.compare_value}}</span></div>'
            },
            {
                displayName: '描述',
                cellTemplate: '<div style="line-height: 30px;padding-left: 10px;vertical-align: middle;width:100%;text-overflow: ellipsis;overflow: hidden;white-space: nowrap"><span title="{{row.entity.description}}">{{row.entity.description}}</span></div>'
            },
            {
                displayName: '描述', width: 150,
                cellTemplate: '<div style="line-height: 30px;padding-left: 10px;vertical-align: middle;width:100%;text-overflow: ellipsis;overflow: hidden;white-space: nowrap"><span title="{{row.entity.when_created}}">{{row.entity.when_created}}</span></div>'
            },
            {
                displayName: '操作', width: 150,
                cellTemplate: '<div style="width:100%;padding-top:5px;text-align: center;">' +
                '<span title="编辑" class="fa fa-pencil fa-lg onoperate " style="color:blue;cursor: pointer;" ng-click="modifyItem(row.entity)"></span>&emsp;' +
                '<span title="删除" class="fa fa-trash-o fa-lg onoperate" style="color:red;cursor: pointer" ng-click="deleteItem(row)"></span>' +
                '</div>'
            }
        ]
    };

    $scope.modifyItem = function (rowEntity) {
        var modalInstance = $modal.open({
            templateUrl: static_url + 'client/views/taskManagement/customItemModify.html',
            windowClass: 'dialog_custom_item',
            controller: 'customItemModifyCtrl',
            backdrop: 'static',
            resolve: {
                itemObj: function () {
                    return angular.copy(rowEntity);
                }
            }
        });
        modalInstance.result.then(function () {
            $scope.searchObj();
        })
    };

    $scope.deleteItem = function (row) {
        confirmModal.open({
            text: "请确认是否删除该自定义巡检项",
            confirmClick: function () {
                loading.open();
                taskService.delete_custom_item({}, row.entity, function (res) {
                    loading.close();
                    if (res.result) {
                        msgModal.open("success", "删除成功！");
                        $scope.searchObj();
                    }
                    else {
                        errorModal.open(res.data);
                    }
                })
            }
        })
    };
});