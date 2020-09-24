controllers.controller("appList", ["$scope", "sysService", "errorModal", "loading", "$modal", "confirmModal","msgModal", function ($scope, sysService, errorModal, loading, $modal, confirmModal,msgModal) {
    $scope.appList = [];
    $scope.filterObj = {
        appName: ""
    };
    $scope.searchApp = function () {
        sysService.search_app_list({}, $scope.filterObj, function (res) {
            if (res.result)
                $scope.appList = res.data;
            else
                errorModal.open(res.data);
        })
    };
    $scope.searchApp();
    $scope.gridOption = {
        data: "appList",
        columnDefs: [
            {field: "name", displayName: "业务名称"},
            {field: "when_created", displayName: "添加时间"},
            {
                displayName: "操作", width: 80,
                cellTemplate: '<div style="width: 100%;padding-top:5px;text-align: center">' +
                '<span  ng-click="deleteApp(row)" class="label label-sm label-danger label-btn button-radius">删除</span>' +
                '</div>'
            }
        ]
    };

    $scope.deleteApp = function (row) {
        confirmModal.open({
            text: "请确认是否要删除该业务！",
            confirmClick: function () {
                sysService.delete_app({
                    app_id: row.entity.id
                }, {}, function (res) {
                    if (res.result) {
                        $scope.searchApp();
                    }
                    else {
                        errorModal.open(res.data);
                    }
                })
            }
        })
    };

    $scope.addApp = function () {
        var modalInstance = $modal.open({
            templateUrl: static_url + 'client/views/sysManagement/appAdd.html',
            windowClass: 'dialogApp',
            controller: 'appAdd',
            backdrop: 'static'
        });
        modalInstance.result.then(function () {
            $scope.searchApp();
        })
    };

    $scope.syncApp = function () {
        loading.open();
        sysService.sync_app({}, {}, function (res) {
            loading.close();
            if (res.result) {
                msgModal.open("success", "同步完成！");
            }
            else {
                errorModal.open(res.data);
            }
        })
    }
}]);