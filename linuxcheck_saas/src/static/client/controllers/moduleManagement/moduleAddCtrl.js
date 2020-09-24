controllers.controller("moduleAddCtrl", function ($scope, moduleService, loading, msgModal, errorModal) {
    $scope.moduleObj = {
        name: "",
        base_module_id: "",
        description: "",
        check_item_list: [],
        created_by: current_user,
        custom_item_list: [],
        os_type: ""
    };

    $scope.customObj = {
        is_checked: true,
        isShow: true
    };
    $scope.customItemList = [];
    $scope.isSecond = false;

    $scope.moduleList = [];
    $scope.itemList = [];
    $scope.menuList = [];

    $scope.osTypeList = [
        {id: 1, text: "CentOS、Redhat系统"},
        {id: 2, text: "SUSE系统"}
    ];

    $scope.changeType = function () {
        loading.open();
        moduleService.get_module_list({}, {type_id: $scope.moduleObj.os_type}, function (res) {
            loading.close();
            if (res.result) {
                $scope.moduleList = res.data;
            }
            else {
                errorModal.open(res.data);
            }
        })
    };

    $scope.moduleOption = {
        data: "moduleList",
        modelData: "moduleObj.base_module_id"
    };

    $scope.osTypeOption = {
        data: "osTypeList",
        modelData: "moduleObj.os_type"
    };

    $scope.changeModule = function () {
        if($scope.moduleObj.os_type == ""){
            errorModal.open("请先选择系统类型！")
        }
        loading.open();
        moduleService.get_module_item_list({module_id: $scope.moduleObj.base_module_id}, {}, function (res) {
            loading.close();
            if (res.result) {
                $scope.itemList = res.data;
                $scope.menuList = res.menu_list;
                $scope.customItemList = res.custom_item_list;
            }
            else {
                errorModal.open(res.data);
            }
        })
    };

    $scope.goNext = function () {
        var errors = validateObj();
        if (errors.length > 0) {
            errorModal.open(errors);
            return;
        }
        $scope.isSecond = true;
    };
    $scope.goBack = function () {
        $scope.isSecond = false;
    };

    $scope.openDetail = function (i) {
        i.isShow = !i.isShow;
    };

    $scope.changeMenuOne = function (i) {
        angular.forEach(i.menu_two, function (u) {
            u.is_checked = i.is_checked;
        });
        angular.forEach($scope.itemList, function (u) {
            if (u.menu_one === i.menu_one) {
                u.is_checked = i.is_checked;
            }
        })
    };

    $scope.changeMenuTwo = function (i) {
        angular.forEach($scope.itemList, function (u) {
            if (u.menu_two === i.name) {
                u.is_checked = i.is_checked;
            }
        })
    };

    $scope.changCustomItem = function (i) {
        angular.forEach($scope.customItemList, function (u) {
            u.is_checked = i.is_checked;
        })
    };

    $scope.confirm = function () {
        var item_count = 0;
        angular.forEach($scope.itemList, function (i) {
            if (i.is_checked) {
                item_count += 1;
            }
        });
         angular.forEach($scope.customItemList, function (i) {
            if (i.is_checked) {
                item_count += 1;
            }
        });
        if (item_count === 0) {
            msgModal.open("error", "请至少选择一项");
            return;
        }
        loading.open();
        $scope.moduleObj.check_item_list = angular.copy($scope.itemList);
        $scope.moduleObj.custom_item_list = angular.copy($scope.customItemList);
        moduleService.create_module({}, $scope.moduleObj, function (res) {
            loading.close();
            if (res.result) {
                msgModal.open("success", "创建成功！");
                window.location.href = "#/moduleList";
            }
            else {
                errorModal.open(res.data);
            }
        })
    };

    var validateObj = function () {
        var errors = [];
        if ($scope.moduleObj.name === "") {
            errors.push("模板名称不能为空!");
        }
        if ($scope.moduleObj.os_type === ""){
            errors.push("系统类型不能为空!");
        }
        if ($scope.moduleObj.base_module_id === "") {
            errors.push("基准模板未选择!");
        }
        return errors;
    }

});