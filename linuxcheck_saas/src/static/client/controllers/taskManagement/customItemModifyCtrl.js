controllers.controller("customItemModifyCtrl", function ($modalInstance, $scope, loading, errorModal, taskService, msgModal, itemObj) {
    $scope.args = itemObj;
    if(itemObj.os_type === "1") {
        $scope.args.os_name = "CentOS、Redhat系统"
    }
    else if (itemObj.os_type === "2"){
        $scope.args.os_name = "SUSE系统"
    }
    else{
        $scope.args.os_name = "未知"
    }
    $scope.title = "编辑自定义巡检项";
        $scope.osTypeList = [
        {id: 1, text: "CentOS、Redhat系统"},
        {id: 2, text: "SUSE系统"}
    ];
    $scope.osTypeOption = {
        data: "osTypeList",
        modelData: "moduleObj.os_type"
    };
    $scope.confirm = function () {
        var errors = validateObj();
        if (errors.length > 0) {
            errorModal.open(errors);
            return;
        }
        loading.open();
        taskService.modify_custom_item({}, $scope.args, function (res) {
            loading.close();
            if (res.result) {
                msgModal.open("success", "修改成功");
                $modalInstance.close();
            }
            else {
                errorModal.open([res.data]);
            }
        })
    };

    var validateObj = function () {
        var errors = [];
        if ($scope.args.os_type === "") {
            errors.push("系统类型不能为空！");
        }
        if ($scope.args.name === "") {
            errors.push("巡检字段不能为空！");
        }
        if ($scope.args.cn_name === "") {
            errors.push("巡检项名称不能为空")
        }
        if ($scope.args.script_content === "") {
            errors.push("巡检脚本不能为空");
        }
        return errors;
    };

    $scope.cancel = function () {
        $modalInstance.dismiss("cancel");
    }
});