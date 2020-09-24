controllers.controller("selectGroupsCtrl", ["$scope", "$filter", "taskService", "errorModal", "confirmModal", "loading", "$modalInstance", function ($scope, $filter, taskService, errorModal, confirmModal, loading, $modalInstance) {
    $scope.filterObj = {
        group_name: ""
    };
    $scope.title = "动态分组";

    $scope.cancel = function () {
        $modalInstance.dismiss("cancel");
    };

    $scope.all_group = [];
    $scope.Pagingdata = [];
    $scope.totalSerItems = 0;

    $scope.pagingOptions = {
        pageSizes: [10,50,100],
        pageSize: "10",
        currentPage: 1
    };

    $scope.groupList = [];
    $scope.init = function () {
        loading.open();
        taskService.search_dynamic_group_list({}, {}, function (res) {
            loading.close();
            if(res.result){
                $scope.all_group = res.data;
                $scope.groupList = angular.copy($scope.all_group);
                $scope.pagingOptions.currentPage = 1;
                $scope.getPagedDataAsync($scope.pagingOptions.pageSize, $scope.pagingOptions.currentPage);
            }
            else{
                errorModal.open(res.data);
            }
        })
    };
    $scope.init();

    $scope.getPagedDataAsync = function (pageSize, page) {
        $scope.setPagingData($scope.groupList ? $scope.groupList : [], pageSize, page);
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

    $scope.gridOption = {
        data: "Pagingdata",
        enablePaging: true,
        showFooter: true,
        enableSorting: false,
        pagingOptions: $scope.pagingOptions,
        totalServerItems: 'totalSerItems',
        enableColumnResize: true,
        enableRowSelection: true,
        checkboxCellTemplate: '<div style="width:100%;padding:9px 5px;"><input type="checkbox" ng-change="changeSelect(row.entity)" ng-model="row.entity.is_checked" /></div>',
        checkboxHeaderTemplate: '<div style="width:100%;padding:9px 5px;"><input type="checkbox" ng-model="all_selection.is_select_all" ng-change="selectAll()" /></div>',
        showSelectionCheckbox: true,
        selectWithCheckboxOnly: true,
        // multiSelect: true,
        columnDefs: [
            {field: "app_name", displayName: "业务名称"},
            {field: "group_name", displayName: "分组名称"}
        ]
    };

    // 勾选动态分组
    $scope.selectItem = [];
    $scope.all_selection = {is_select_all: false};
    $scope.changeSelect = function (rowEntity) {
        if(rowEntity.is_checked){
            $scope.selectItem.push(rowEntity);
        } else {
            var index = $scope.selectItem.indexOf(rowEntity);
            $scope.selectItem.splice(index, 1);
        }
    };

    // 动态分组全选
    $scope.selectAll = function () {
        angular.forEach($scope.Pagingdata, function (i) {
            i.is_checked = $scope.all_selection.is_select_all;
        });
        angular.forEach($scope.groupList, function (i) {
            i.is_checked = $scope.all_selection.is_select_all;
        });
        if ($scope.all_selection.is_select_all) {
            $scope.selectItem = angular.copy($scope.groupList);
        } else {
            $scope.selectItem = [];
        }
    };

    // 动态分组筛选
    $scope.search_group = function () {
        if($scope.filterObj.group_name == ""){
            $scope.groupList = angular.copy($scope.all_group);
        } else {
            $scope.groupList = [];
            angular.forEach($scope.all_group, function (obj) {
                if(obj.group_name.toUpperCase().indexOf($scope.filterObj.group_name.toUpperCase()) > -1){
                    $scope.groupList.push(obj);
                }
            })
        }
        $scope.pagingOptions.currentPage = 1;
        $scope.getPagedDataAsync($scope.pagingOptions.pageSize, $scope.pagingOptions.currentPage);
    };

    // 确定
    $scope.confirm = function () {
        $modalInstance.close($scope.selectItem);
    }
}]);