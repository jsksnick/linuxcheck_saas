controllers.controller("appAdd", ["$scope", "sysService", "loading", "$modalInstance", "errorModal", function ($scope, sysService, loading, $modalInstance, errorModal) {
    $scope.appList = [];
    $scope.rowSection = [];
    $scope.gridOption = {
        data: "appList",
        multiSelect: true,
        enableRowSelection: true,
        showSelectionCheckbox: true,
        selectedItems: $scope.rowSection,
        selectWithCheckboxOnly: true,
        columnDefs: [
            {field: "app_name", displayName: "业务名称"}
        ]
    };

    $scope.getAppList = function () {
        loading.open("", ".addApp");
        sysService.get_user_app_list({}, {}, function (res) {
            loading.close(".addApp");
            if (res.result) {
                $scope.appList = res.data;
            }
            else {
                errorModal.open(res.data);
            }
        })
    };
    $scope.getAppList();
    $scope.confirm = function () {
        sysService.add_app({}, $scope.rowSection, function (res) {
            if (res.result) {
                $modalInstance.close();
            }
            else
                errorModal.open(res.data);
        })
    };

    $scope.cancel = function () {
        $modalInstance.dismiss("cancel");
    }
}]);