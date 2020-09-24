controllers.controller("selectTopoCtrl", ["$scope", "$filter", "taskService", "errorModal", "confirmModal", "loading", "$modalInstance", function ($scope, $filter, taskService, errorModal, confirmModal, loading, $modalInstance) {
    $scope.zTreeOptions = {
        check: {
            enable: true,
            // 是否勾选对上下级是否生效
            chkboxType: { "Y": "s","N": "s" }
        },
        data: {
            key: {
                name: "bk_inst_name",
                children: "child",
                isParent: "isParent",
                checked: "checked",
                chkDisabled: "chkDisabled"
            }
        },
        // 下拉
        asyncUrl: site_url + 'search_app_topo',
        autoParam: ["bk_inst_id=bk_inst_id", 'bk_biz_id=bk_biz_id', 'topo_type=topo_type',
            'checked=checked', "bk_biz_name=bk_biz_name", "chkDisabled=chkDisabled"],
        // 勾选
        onCheck: function (event, treeId, treeNode) {
            if(treeNode.checked){
                $scope.check_topo_node(event, treeId, treeNode);
            } else {
                // 取消勾选子节点取消禁止同时取消勾选
                treeNode.isSelect = false;
                var treeObj = $.fn.zTree.getZTreeObj("businessTopo");
                angular.forEach(treeNode.child, function (nodeObj) {
                    treeObj.setChkDisabled(nodeObj, false, false, true) ;
                    treeObj.checkNode(nodeObj,false,true)
                });
            }
        },
        view: {showIcon: false, showLine: false}
    };

    $scope.search_business_topo = function () {
        loading.open();
        taskService.get_all_business({}, {}, function (res) {
            loading.close();
            if (res.result) {
                $scope.businessTopo = res.data;
            } else {
                errorModal.open(res.data);
            }
        })
    };
    $scope.search_business_topo();

    $scope.check_topo_node = function (event, treeId, treeNode) {
        treeNode.isSelect = true;
        // 模块最小单元
        if(treeNode.bk_obj_name == "module"){
            return
        }

        var treeObj = $.fn.zTree.getZTreeObj("businessTopo");
        treeObj.refresh();
        if(treeNode.child.length > 0){
            angular.forEach(treeNode.child, function (nodeObj) {
                treeObj.setChkDisabled(nodeObj, true, false, true) ;
            });
        }


    };

    // 业务以外节点直接展开
    $scope.modify_open_status = function (treeNode) {
        treeNode.open = true;
        angular.forEach(treeNode.child, function (obj) {
            obj.open = true;
            if(obj.child.length > 0){
                $scope.modify_open_status(obj.child);
            }
        })
    };

    // 选择整个业务并展开
    $scope.check_app_topo = function (treeNode) {
        loading.open();
        taskService.check_app_topo({}, treeNode, function (res) {
            loading.close();
            if(res.data.length === 0){
                return;
            }
            var treeObj = $.fn.zTree.getZTreeObj("businessTopo");
            treeObj.removeChildNodes(treeNode);
            treeObj.addNodes(treeNode, res.data);
            angular.forEach(treeNode.child, function (nodeObj) {
                treeObj.setChkDisabled(nodeObj, true, false, true) ;
            });
        })
    };

    $scope.cancel = function () {
        $modalInstance.dismiss("cancel");
    };

    $scope.confirm = function () {
        var item = [];
        var treeObj = $.fn.zTree.getZTreeObj("businessTopo");
        var select_node = treeObj.getCheckedNodes(true);
        angular.forEach(select_node, function (obj) {
            item.push({
                "bk_biz_id": obj.bk_biz_id,
                "bk_biz_name": obj.bk_biz_name,
                "bk_inst_id": obj.bk_inst_id,
                "bk_inst_name": obj.bk_inst_name,
                "bk_obj_id": obj.bk_obj_id,
                "bk_obj_name": obj.bk_obj_name,
                "node_name": obj.node_name
            })
        });
        $modalInstance.close(item);
    };

}]);