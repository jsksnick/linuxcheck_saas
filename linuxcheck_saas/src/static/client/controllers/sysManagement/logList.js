controllers.controller('logList', ["$scope", "errorModal", "sysService", "$filter", "$modal", "loading", function ($scope, errorModal, sysService, $filter, $modal, loading) {
    var dateStart = new Date();
    var dateEnd = new Date();
    $scope.DateStart = dateStart.setDate(dateStart.getDate() - 29);
    $scope.DateEnd = dateEnd.setDate(dateEnd.getDate() + 1);

    $scope.recordList = [];
    $scope.Pagingdata = [];
    $scope.totalSerItems = 0;

    $scope.pagingOptions = {
        pageSizes: [10, 50, 100],
        pageSize: "10",
        currentPage: 1
    };

    $scope.filter = {
        operator: "",
        operateType: "00",
        whenStart: $filter('date')($scope.DateStart, 'yyyy-MM-dd'),
        whenEnd: $filter('date')($scope.DateEnd, 'yyyy-MM-dd')
    };

    $scope.SearchObj = function () {
        loading.open();
        sysService.search_log({}, $scope.filter, function (res) {
            loading.close();
            $scope.recordList = res.data;
            $scope.pagingOptions.currentPage = 1;
            $scope.getPagedDataAsync($scope.pagingOptions.pageSize, $scope.pagingOptions.currentPage);
        })
    };
    $scope.SearchObj();

    $scope.getPagedDataAsync = function (pageSize, page) {
        $scope.setPagingData($scope.recordList ? $scope.recordList : [], pageSize, page);
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

    $scope.gridoption = {
        data: "Pagingdata",
        enablePaging: true,
        showFooter: true,
        pagingOptions: $scope.pagingOptions,
        totalServerItems: 'totalSerItems',
        columnDefs: [
            {field: 'operator', displayName: '操作者', width: 80},
            {field: 'operate_obj', displayName: '操作对象', width: 80},
            {field: 'operate_type_name', displayName: '操作类型', width: 200},
            {field: 'when_created', displayName: '操作时间', width: 200},
            {field: 'operate_summary', displayName: '概要'},
            {
                displayName: '操作', width: 80,
                cellTemplate: '<div style="width:100%;padding-top:5px;text-align: center">' +
                '<span ng-if="row.entity.operate_type!=\'api\' " class="label label-btn button-radius label-sm label-primary" ' +
                'ng-click="openDetail(row.entity)">详情</span>' +
                '<span ng-if="row.entity.operate_type==\'api\'" class="label label-sm label-primary button-radius">详情</span>' +
                '</div>'
            }
        ]
    };
    $scope.openDetail = function (rowEntity) {
        var modalInstance = $modal.open({
            templateUrl: static_url + 'client/views/sysManagement/logDetail.html',
            windowClass: 'logDetail',
            controller: 'logDetail',
            backdrop: 'static',
            resolve: {
                objectItem: function () {
                    return angular.copy(rowEntity);
                }
            }
        });
    }
}]);
