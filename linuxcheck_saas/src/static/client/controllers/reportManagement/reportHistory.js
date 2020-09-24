controllers.controller("reportHistory", function ($scope, reportService, loading, errorModal, $filter, msgModal, confirmModal) {
    var dateStart = new Date();
    var dateEnd = new Date();
    $scope.DateStart = dateStart.setDate(dateStart.getDate() - 30);
    $scope.DateEnd = dateEnd.setDate(dateEnd.getDate());

    $scope.filterObj = {
        task_name: "",
        start_time: $filter('date')($scope.DateStart, 'yyyy-MM-dd'),
        end_time: $filter('date')($scope.DateEnd, 'yyyy-MM-dd')
    };

    $scope.PagingData = [];
    $scope.totalSerItems = 0;

    $scope.pagingOptions = {
        pageSizes: [10, 50, 100],
        pageSize: "10",
        currentPage: 1
    };

    $scope.searchList = function () {
        loading.open();
        reportService.get_report_list({}, $scope.filterObj, function (res) {
            loading.close();
            if (res.result) {
                $scope.reportList = res.data;
                $scope.pagingOptions.currentPage = 1;
                $scope.getPagedDataAsync($scope.pagingOptions.pageSize, $scope.pagingOptions.currentPage);
                if (res.is_checked) {
                    var url_path = window.location.href;
                    if (url_path.indexOf("#/reportHistory") > -1)
                        setTimeout($scope.searchList, 5000);
                }
            }
            else {
                msgModal.open("error", res.data[0]);
            }

        })
    };
    $scope.getPagedDataAsync = function (pageSize, page) {
        $scope.setPagingData($scope.reportList ? $scope.reportList : [], pageSize, page);
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
            {field: "task_name", displayName: "任务名称", width: 200},
            {field: "when_created", displayName: "执行时间", width: 150},
            {field: "summary", displayName: "任务概览"},
            {
                displayName: "任务进度", width: 150,
                cellTemplate: '<div class="progress progress-striped active" style="height:29px;margin-bottom:1px"><div class="progress-bar progress-bar-success" style="width: {{ row.entity.schedule }};line-height: 29px">{{ row.entity.schedule }}</div></div>'
            },
            {
                displayName: "状态", width: 100,
                cellTemplate: '<div style="width:100%;padding-top:5px;text-align: center">' +
                '<span  ng-if="row.entity.status == \'RUNNING\'">' +
                '<i  class="fa fa-spinner fa-pulse"></i>\
                进行中</span>\
                <span  ng-if="row.entity.status == \'COMPLETE\'" >\
                 <i class="fa fa-check color_green"></i>\
                 完成</span>' +
                '</div>'
            },
            {
                displayName: "操作", width: 230,
                cellTemplate: '<div style="width:100%;padding-top:5px;text-align: center">' +
                '<span ng-if="row.entity.status == \'COMPLETE\'" ng-click="openDetail(row.entity)" class="label label-sm label-info label-btn button-radius">详情</span>' +
                '<span ng-if="row.entity.status == \'RUNNING\'" style="box-shadow:none;opacity:0.65" class="label label-sm label-info button-radius">详情</span>' +
                '<span ng-if="row.entity.status == \'COMPLETE\'" ng-click="errorSummary(row.entity)" class="label label-sm label-warning label-btn button-radius" style="margin: 0 5px">错误汇总</span>' +
                '<span ng-if="row.entity.status == \'RUNNING\'" style="box-shadow:none;opacity:0.65" class="label label-sm label-warning button-radius" style="margin: 0 5px">错误汇总</span>' +
                '<span ng-if="row.entity.status == \'COMPLETE\'" ng-click="deleteReport(row.entity)" class="label label-sm label-danger label-btn button-radius">删除</span>' +
                '<span ng-if="row.entity.status == \'RUNNING\'" style="box-shadow:none;opacity:0.65" class="label label-sm label-danger button-radius">删除</span>' +
                '</div>'
            }
        ]
    };

    $scope.openDetail = function (rowEntity) {
        window.location.href = "#/reportServer?report_id=" + rowEntity.id;
    };
    $scope.errorSummary = function (rowEntity) {
        window.location.href = "#/errorSummary?report_id=" + rowEntity.id;
    };
    $scope.deleteReport = function (rowEntity) {
        confirmModal.open({
            text: '是否删除报告？',
            confirmClick: function () {
                reportService.delete_report({}, rowEntity, function (res) {
                    if (res.result) {
                        alert("删除报告成功！");
                        $scope.searchList();
                    }
                    else {
                        msgModal.open("error", res.data[0]);
                    }
                })
            }
        });
    };
});