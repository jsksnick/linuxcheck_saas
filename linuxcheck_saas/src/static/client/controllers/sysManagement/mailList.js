controllers.controller("mailList", ["$scope", "errorModal", "$modal", "loading", "confirmModal", "sysService", function ($scope, errorModal, $modal, loading, confirmModal, sysService) {
    $scope.mail_list = [];
    $scope.args = {
        username: "",
        mailbox: ""
    };
    $scope.PagingData = [];
    $scope.totalSerItems = 0;

    $scope.pagingOptions = {
        pageSizes: [10, 50, 100],
        pageSize: "10",
        currentPage: 1
    };
    $scope.search_mail = function () {
        loading.open();
        sysService.search_mail({}, $scope.args, function (res) {
            loading.close();
            if (res.result) {
                $scope.mail_list = res.data;
                $scope.pagingOptions.currentPage = 1;
                $scope.getPagedDataAsync($scope.pagingOptions.pageSize, $scope.pagingOptions.currentPage);
            }
            else {
                errorModal.open(res.data);
            }
        })
    };
    $scope.getPagedDataAsync = function (pageSize, page) {
        $scope.setPagingData($scope.mail_list ? $scope.mail_list : [], pageSize, page);

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

    $scope.search_mail();


    $scope.add_mail = function () {
        var modalInstance = $modal.open({
            templateUrl: static_url + 'client/views/sysManagement/mailAdd.html',
            windowClass: 'dialog_custom',
            controller: 'mailAdd',
            backdrop: 'static',
            resolve: {
                objectItem: function () {
                    return $scope.username
                }
            }
        });
        modalInstance.result.then(function (res) {
            for (var i in res) {
                $scope.mail_list.unshift(res[i]);
            }
            $scope.getPagedDataAsync($scope.pagingOptions.pageSize, $scope.pagingOptions.currentPage);
        })
    };

    $scope.modify_mail = function (row) {
        var modalInstance = $modal.open({
            templateUrl: static_url + 'client/views/sysManagement/mailAdd.html',
            windowClass: 'dialog_custom',
            controller: 'mailModify',
            backdrop: 'static',
            resolve: {
                objectItem: function () {
                    return row.entity;
                }
            }
        });
        modalInstance.result.then(function (res) {
            row.entity.account = res.account;
            row.entity.mailbox = res.mailbox;
            row.entity.when_created = res.when_created;
        })
    };

    $scope.delete_mail = function (row) {
        var id = row.entity.id;
        confirmModal.open({
            text: "确认删除该邮箱吗？",
            confirmClick: function () {
                loading.open();
                sysService.delete_mail({id: id}, {}, function (res) {
                    if (res.result) {
                        loading.close();
                        $scope.mail_list.splice(row.rowIndex, 1);
                        $scope.getPagedDataAsync($scope.pagingOptions.pageSize, $scope.pagingOptions.currentPage);
                    }
                    else {
                        errorModal.open(res.data.split(";"));
                    }
                })
            }
        })
    };


    $scope.gridOption = {
        data: 'PagingData',
        enablePaging: true,
        showFooter: true,
        pagingOptions: $scope.pagingOptions,
        totalServerItems: 'totalSerItems',
        columnDefs: [
            {field: 'account', displayName: '用户名'},
            {field: 'mailbox', displayName: '邮箱地址'},
            {field: 'when_created', displayName: '添加时间'},
            {
                displayName: '操作', width: 180,
                cellTemplate: '<div style="width:100%;text-align: center;padding-top: 5px;z-index: 1">' +
                '<span ng-click="delete_mail(row)" class="label label-danger button-radius" style="min-width:50px;margin-left: 5px;cursor:pointer;">删除</span>' +
                '</div>'
            }

        ]
    };
}]);



