controllers.controller("sysSet", function ($scope, sysService, loading, msgModal, errorModal) {
    $scope.sysObj = {};
    $scope.isModify = false;
    $scope.oldSet = {};
    $scope.init = function () {
        loading.open();
        sysService.get_settings({}, {}, function (res) {
            loading.close();
            if (res.result) {
                $scope.sysObj = res.data;
                $scope.oldSet = angular.copy($scope.sysObj);
            }
            else {
                errorModal.open(res.data);
            }
        })
    };

    $scope.init();

    $scope.modify = function () {
        $scope.isModify = true;
    };

    $scope.cancel = function () {
        $scope.isModify = false;
        $scope.sysObj = angular.copy($scope.oldSet);
    };

    $scope.confirm = function () {
        var errors = validateObj();
        if (errors.length > 0) {
            errorModal.open(errors);
            return;
        }
        loading.open();
        sysService.set_settings({}, $scope.sysObj, function (res) {
            loading.close();
            if (res.result) {
                msgModal.open("success", "修改成功");
                $scope.oldSet = angular.copy($scope.sysObj);
                $scope.isModify = false;
            }
            else {
                errorModal.open(res.data);
            }
        })
    };

    var validateObj = function () {
        var errors = [];
        if ($scope.sysObj.config_account == "") {
            errors.push("配置执行帐号不能为空！");
        }
        if ($scope.sysObj.report_save + "abc" == "abc") {
            errors.push("报告保留份数不能为空！");
        }
        else {
            if ((!CWApp.isNum($scope.sysObj.report_save)) || $scope.sysObj.report_save < 0) {
                errors.push("报告保留份数必须为大于等于0的整数")
            }
        }
        return errors;
    }
});