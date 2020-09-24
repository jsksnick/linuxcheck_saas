controllers.controller("home", ["msgModal", "$scope", "loading", "sysService", function (msgModal, $scope, loading, sysService) {
    $scope.countObj = {};
    $scope.reportList = [];
    $scope.taskList = [];

    $scope.taskReports = {
        data: "taskList",
        chart: {type: 'line'},
        title: {text: '每月历史巡检次数统计', enabled: true},
        xAxis: {
            categories: []
        },
        //提示框位置和显示内容
        tooltip: {
            pointFormat: '<tr><td style="color:{series.color};padding:0">{series.name}: </td>' +
            '<td style="padding:0"><b>{point.y:f}</b></td></tr>',
            headerFormat: ""
        }
    };

    loading.open();
    sysService.get_count_obj({}, {}, function (res) {
        loading.close();
        if (res.result) {
            $scope.countObj = res.data;
            $scope.taskList = res.task_list.data;
            $scope.taskReports.xAxis.categories = res.task_list.categories;
            $scope.reportList = res.report_list;
        }
    });

    $scope.openReportDetail = function (id) {
        window.location.href = "#/reportServer?report_id=" + id;
    }

}]);
