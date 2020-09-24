controllers.controller("selectServersCtrl", ["$scope", "$filter", "sysService", "errorModal", "confirmModal", "loading", "$modalInstance", "itemObj", function ($scope, $filter, sysService, errorModal, confirmModal, loading, $modalInstance, itemObj) {
    $scope.serverList = [];
    $scope.selectIndex = {value: "1"};
    $scope.businessTopo = [];
    $scope.filterObj = {
        ip: "",
        is_exact: true
    };
    $scope.all_server = [];
    $scope.Pagingdata = [];
    $scope.totalSerItems = 0;

    $scope.pagingOptions = {
        pageSizes: [7, 50, 100],
        pageSize: "7",
        currentPage: 1
    };

    $scope.changeType = function (i) {
        if (i === 1) {
            $scope.all_selection.selectAll = false;
            $scope.selectedItems = [];
            $scope.filterObj.ip = "";
            $scope.serverList = angular.copy($scope.all_server);
            $scope.pagingOptions.currentPage = 1;
            $scope.getPagedDataAsync($scope.pagingOptions.pageSize, $scope.pagingOptions.currentPage);
        }
        else if (i === 2 && $scope.businessTopo.length === 0) {
            $scope.search_business_topo();
        }
    };
    $scope.search_business_servers = function () {
        loading.open("", ".server-load");
        sysService.search_business_servers({}, {"type_id": itemObj}, function (res) {
            loading.close(".server-load");
            if (res.result) {
                $scope.all_server = angular.copy(res.data);
                $scope.serverList = res.data;
                $scope.pagingOptions.currentPage = 1;
                $scope.getPagedDataAsync($scope.pagingOptions.pageSize, $scope.pagingOptions.currentPage);
            }
            else {
                errorModal.open(res.data)
            }
        })
    };
    setTimeout($scope.search_business_servers, 500);

    $scope.getPagedDataAsync = function (pageSize, page) {
        $scope.setPagingData($scope.serverList ? $scope.serverList : [], pageSize, page);
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
    $scope.selectedItems = [];
    $scope.gridOption = {
        data: "Pagingdata",
        enablePaging: true,
        enableSorting: false,
        showFooter: true,
        pagingOptions: $scope.pagingOptions,
        totalServerItems: 'totalSerItems',
        enableColumnResize: true,
        enableRowSelection: true,
        // selectedItems: $scope.selectedItems,
        checkboxCellTemplate: '<div style="width:100%;padding:9px 5px;"><input type="checkbox" ng-change="change_select(row.entity)" ng-model="row.entity.is_checked" /></div>',
        checkboxHeaderTemplate: '<div style="width:100%;padding:9px 5px;"><input type="checkbox" ng-model="all_selection.is_select_all" ng-change="selectAll()" /></div>',
        showSelectionCheckbox: true,
        selectWithCheckboxOnly: true,
        // multiSelect: true,
        columnDefs: [
            {field: "source_name", displayName: "区域名称"},
            {field: "ip", displayName: "IP"},
            {field: "bk_os_name", displayName: "操作系统"}
        ]
    };
    $scope.all_selection = {is_select_all: false};
    $scope.selectAll = function () {
        angular.forEach($scope.Pagingdata, function (i) {
            i.is_checked = $scope.all_selection.is_select_all;
        });
        angular.forEach($scope.serverList, function (i) {
            i.is_checked = $scope.all_selection.is_select_all;
        });
        if ($scope.all_selection.is_select_all) {
            $scope.selectedItems = angular.copy($scope.serverList);
        }
        else {
            $scope.selectedItems = [];
        }
    };

    $scope.change_select = function (rowEntity) {
        if (rowEntity.is_checked) {
            $scope.selectedItems.push(rowEntity);
        }
        else {
            var tmp = angular.copy($scope.selectedItems);
            for (var i in $scope.selectedItems) {
                if ($scope.selectedItems[i].ip === rowEntity.ip && $scope.selectedItems[i].source === rowEntity.source) {
                    tmp.splice(i, 1);
                    break;
                }
            }
            $scope.selectedItems = angular.copy(tmp);
        }

    };

    $scope.search_business_topo = function () {
        loading.open("", ".server-load");
        sysService.get_all_business({}, {}, function (res) {
            loading.close(".server-load");
            if (res.result) {
                $scope.businessTopo = res.data;
            }
            else {
                errorModal.open(res.data);
            }
        })
    };
    $scope.zTreeOptions = {
        check: {
            enable: true
        },
        data: {
            key: {
                name: "bk_inst_name",
                children: "child",
                isParent: "isParent",
                checked: "checked"
            }
        },
            asyncUrl: site_url + 'search_business_topo/?os_type=' + itemObj,
        autoParam: ["bk_inst_id=bk_inst_id", 'bk_biz_id=bk_biz_id', 'topo_type=topo_type' ,'checked=checked'],
        onCheck: function (event, treeId, treeNode) {
            if (treeNode.checked)
                $scope.check_all_servers(event, treeId, treeNode);
        },
        view: {showIcon: false, showLine: false}
    };

    $scope.check_all_servers = function (event, treeId, treeNode) {
        if (treeNode.is_open_all) {
            return;
        }
        treeNode.is_open_all = true;
        if (treeNode.bk_obj_name === "IP") {
            return;
        }
        if (treeNode.topo_type === 1 && treeNode.child.length === 0) {
            $scope.get_app_servers(treeNode)
        }
        else if (treeNode.child.length > 0 && treeNode.child[0].bk_obj_name === 'IP') {
        }
        else {
            loading.open("", ".server-load");
            sysService.get_check_servers({'os_type': itemObj}, treeNode, function (res) {
                loading.close(".server-load");
                if (res.data.length === 0) {
                    return;
                }
                // treeNode.child = res.data;
                var treeObj = $.fn.zTree.getZTreeObj("businessTopo");
                treeObj.removeChildNodes(treeNode);
                for (var i = 0; i < res.data.length; i++) {
                    // treeObj.expandNode(treeNode, true, true, true);
                    treeObj.addNodes(treeNode, res.data[i]);
                }
            })
        }
    };

    $scope.get_app_servers = function (treeNode) {
        loading.open("", ".server-load");
        sysService.get_app_check_servers({"type_id": itemObj}, treeNode, function (res) {
            loading.close(".server-load");
            if (res.data.length === 0) {
                return;
            }
            var treeObj = $.fn.zTree.getZTreeObj("businessTopo");
            treeObj.removeChildNodes(treeNode);
            // treeObj.expandNode(treeNode, true, true, true);
            treeObj.addNodes(treeNode, res.data);
            // treeNode.child = res.data;
            // treeNode.open = true;
            // treeObj.updateNode(treeNode);
            // treeNode.open = true;
        })
    };

    $scope.moduleServers = [];

    $scope.selectServers = [];
    $scope.confirm = function () {
        if ($scope.selectIndex.value == '1') {
            $modalInstance.close($scope.selectedItems);
        }
        else {
            var tmp = [];
            var treeObj = $.fn.zTree.getZTreeObj("businessTopo");
            var select_servers = treeObj.getCheckedNodes(true);
            var items = [];
            for (var i = 0; i < select_servers.length; i++) {
                if (select_servers[i].bk_obj_name === "IP") {
                    var oneObj = select_servers[i].ip + "s" + select_servers[i].source;
                    if (tmp.indexOf(oneObj) < 0) {
                        items.push(select_servers[i]);
                        tmp.push(oneObj);
                    }
                }
            }
            $modalInstance.close(items);
        }
    };

    $scope.search_ip = function () {
        $scope.serverList = [];
        var filter_list = $scope.filterObj.ip.trim().split(" ");
        var ids = [];
        var real_filter = $filter("filter")(filter_list, function (i) {
            return i.trim() !== "";
        });
        if (real_filter.length === 0) {
            real_filter = [""];
        }
        angular.forEach(real_filter, function (i) {
            if ($scope.filterObj.is_exact) {
                angular.forEach($scope.all_server, function (u) {
                    if (u.ip === i && $scope.serverList.indexOf(u) < 0) {
                        $scope.serverList.push(u);
                    }
                })
            }
            else {
                angular.forEach($scope.all_server, function (u) {
                    if (u.ip.indexOf(i) > -1 && $scope.serverList.indexOf(u) < 0) {
                        $scope.serverList.push(u);
                    }
                })
            }
        });
        $scope.all_selection.is_select_all = false;
        $scope.selectAll();
        $scope.selectedItems.splice(0, $scope.selectedItems.length);
        $scope.pagingOptions.currentPage = 1;
        $scope.getPagedDataAsync($scope.pagingOptions.pageSize, $scope.pagingOptions.currentPage);
    };

    $scope.cancel = function () {
        $modalInstance.dismiss("cancel");
    };
}]);