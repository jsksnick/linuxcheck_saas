controllers.controller("reportServerDetail", function ($scope, $rootScope, reportService, errorModal, loading) {
    $scope.question_error_list = [];
    $scope.a = {
        is_show: true
    };
    $scope.error_list = [];
    $scope.menu_list = [];
    $scope.summary = "";
    $scope.initDetails = function () {
        loading.open();
        reportService.get_report_server_detail_by_id({}, $scope.serverObj, function (res) {
            loading.close();
            if (res.result) {
                $scope.menu_list = res.menu_list;
                $scope.error_list = res.error_list;
                $scope.summary = res.summary;
                setTimeout(function () {
                    $scope.val_title()
                },200)
            }
            else {
                errorModal.open(res.data);
            }
        })
    };

    $scope.initDetails();


    $scope.goBack = function () {
        $rootScope.isShowDetail = false;
    };

    $scope.errorOption = {
        data: "error_list",
        title: {text: '问题严重程度统计', enabled: true},
        unit: "",
        size: "200px"
    };

    $scope.openTitle = function (i) {
        i.is_show = !i.is_show;
    };
    $scope.export = function () {
        var tempForm = document.createElement("form");
        tempForm.id = "tempForm1";
        tempForm.method = "post";
        //url
        tempForm.action = "export_check_server/?report_id=" + $scope.report_id + "&ip=" + $scope.serverObj.ip_address;
        tempForm.target = '导出报表';
        var hideInput = document.createElement("input");
        hideInput.type = "hidden";
        //传入参数名,相当于get请求中的content=
        hideInput.name = "content";
        //传入传入数据，只传递了一个参数内容，实际可传递多个。
        hideInput.value = $("#reportDetail").html();
        tempForm.appendChild(hideInput);
        document.body.appendChild(tempForm);
        tempForm.dispatchEvent(new Event("onsubmit"));//chrome
        //必须手动的触发，否则只能看到页面刷新而没有打开新窗口
        tempForm.submit();
        document.body.removeChild(tempForm);
    };
    $scope.val_title = function () {
        $('.new_table td').each(function () {
            $(this).attr('title',$(this).text())
        })
    }
});