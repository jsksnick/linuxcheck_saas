controllers.controller("reportServer", function ($scope, $rootScope, reportService, errorModal, loading) {
    $scope.reportObj = {};
    $scope.serverObj = {};
    $scope.question_list = [];
    $rootScope.isShowDetail = false;
    $scope.serverDetailPage = static_url + "client/views/reportManagement/reportServerDetail.html";
    var tmp = window.location.href.split("=");
    var report_id = 0;
    if (tmp.length === 2) {
        report_id = tmp[1];
    }
    $scope.report_id = report_id;
    $scope.init = function () {
        loading.open();
        reportService.get_report_server_by_id({report_id: report_id}, {}, function (res) {
            loading.close();
            if (res.result) {
                $scope.reportObj = res.data;
                $scope.question_list = res.question_list;
            }
            else {
                errorModal.open(res.data);
            }
        })
    };

    $scope.init();

    $scope.openDetail = function (i) {
        $rootScope.isShowDetail = true;
        $scope.serverObj = angular.copy(i);
    };

    $scope.returnBack = function () {
        window.location.href = "#/reportHistory";
    };

    $scope.openSummary = function (i) {
        i.isOpen = !i.isOpen;
    };

    $scope.chartOption = {
        data: "question_list",
        title: {text: '巡检问题汇总', enabled: true},
        unit: "",
        size: "200px"
    };

    $scope.export = function () {
        var tempForm = document.createElement("form");
        tempForm.id = "tempForm1";
        tempForm.method = "post";
        //url
        tempForm.action = "export_check_server/?report_id=" + report_id ;
        tempForm.target = '导出报表';
        var hideInput = document.createElement("input");
        hideInput.type = "hidden";
        //传入参数名,相当于get请求中的content=
        hideInput.name = "content";
        //传入传入数据，只传递了一个参数内容，实际可传递多个。
        hideInput.value = $("#reportServer").html();
        tempForm.appendChild(hideInput);
        // tempForm.addEventListener("onsubmit", function () {
        //     openWindow('导出报表');
        // });
        document.body.appendChild(tempForm);
        tempForm.dispatchEvent(new Event("onsubmit"));//chrome
        //必须手动的触发，否则只能看到页面刷新而没有打开新窗口
        tempForm.submit();
        document.body.removeChild(tempForm);
    };

    function openWindow(name) {
        window.open('about:blank', name);
    }
});