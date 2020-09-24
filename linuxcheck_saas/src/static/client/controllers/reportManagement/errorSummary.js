controllers.controller('errorSummary', ["$scope", "taskService", "loading", "confirmModal", "msgModal", "$modal","$stateParams","$timeout","$compile", "reportService", "errorModal", function ($scope, taskService, loading, confirmModal, msgModal, $modal,$stateParams,$timeout,$compile, reportService, errorModal) {
    $scope.rp_data = {};
    $scope.summary_data = [];
    $scope.report_id = window.location.href.split("=")[1];
    $scope.init = function () {
        loading.open();
        reportService.get_report_error_summary_by_id({report_id: $scope.report_id}, {}, function (res) {
            if (res.result) {
                $scope.rp_data = res.data;
                $scope.summary_data = res.summary_data;
                $scope.lazy_start($scope.summary_data.length);
            }
            else {
                errorModal.open(res.data);
            }
        })
    };
    $scope.init();

    $scope.down_pdf = function () {
        confirmModal.open({
            text: '是否导出PDF？',
            confirmClick: function () {
                var tempForm = document.createElement("form");
                tempForm.id = "tempForm1";
                tempForm.method = "post";
                //url
                tempForm.action = "export_check_error_summary/?report_id=" + $scope.report_id ;
                tempForm.target = '导出报表';
                var hideInput = document.createElement("input");
                hideInput.type = "hidden";
                //传入参数名,相当于get请求中的content=
                hideInput.name = "content";
                //传入传入数据，只传递了一个参数内容，实际可传递多个。
                // hideInput.value = $(".report_server").html();
                hideInput.value = $(".report_server").html()+'<style>div.obj_body>h5{display:none!important;}.obj_body table.error_table{display:table!important;}</style>';
                tempForm.appendChild(hideInput);
                // tempForm.addEventListener("onsubmit", function () {
                //     openWindow('导出报表');
                // });
                document.body.appendChild(tempForm);
                tempForm.dispatchEvent(new Event("onsubmit"));//chrome
                //必须手动的触发，否则只能看到页面刷新而没有打开新窗口
                tempForm.submit();
                document.body.removeChild(tempForm);
            }
        });
    };
    $scope.lazy_start = function (all_length,index) {
        index = index||0;
        if (index>all_length){
            loading.close();
            return
        }
        var end_index = index+20;
        var end_html = '<div ng-repeat="rp in summary_data.slice('+index+','+end_index+') track by $index" ng-init="open={op:true}">'+
                '<div class="obj_title"><h5 ng-click="open.op=!open.op" style="cursor: pointer">{{ rp.name }}' +
            '<i class="fa fa-angle-down" ng-if="open.op"></i><i class="fa fa-angle-up" ng-if="!open.op"></i>' +
            '</h5></div>'+
                '<div class="obj_body">'+
                    '<h5 ng-show="open.op" ng-click="open.op=!open.op" style="cursor: pointer">巡检共发现<span class="error_item">{{ rp.item.length }}</span>项异常</h5>'+
                    '<table class="table error_table" ng-show="!open.op">'+
                        '<tr class="tr_error"><th class="error_table_name">巡检项</th><th class="error_table_value">巡检值</th><th class="error_table_way">关系</th><th class="error_table_compare">推荐值</th></tr>'+
                        '<tr ng-repeat="item in rp.item">'+
                            '<td  ng-bind="item.display" title="{{ item.display }}"></td>'+
                            '<td  cwhtml="item"></td>'+
                            '<td  ng-bind="item.way" title="{{ item.way }}"></td>'+
                            '<td  ng-bind="item.compare" title="{{ item.compare }}"></td>'+
                        '</tr>'+
                    '</table>'+
                '</div>'+
            '</div>';
        var ele = $compile(end_html)($scope);
        if(all_length==0){
            ele='<span class="success_item" style="font-size: 2em">本次巡检未发现异常！</span>'
        }
		if(index==0){
			angular.element('.report_bottom').html(ele);
		}else {
            angular.element('.report_bottom').append(ele);
		}
        $timeout(function () {
                $scope.lazy_start(all_length,end_index)
        },100)
    };


}]);