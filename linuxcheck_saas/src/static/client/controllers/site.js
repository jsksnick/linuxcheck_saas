controllers.controller("site", ["$scope", "sysService", function ($scope, sysService) {
    $scope.menuList = [
        {
            displayName: "首页", iconClass: "fa fa-home fa-lg", url: "#/home"
        },
        {
            displayName: "模板管理", iconClass: "fa fa-th-large fa-lg",
            children: [
                {displayName: "新增模板", url: "#/moduleAdd"},
                {displayName: "模板列表", url: "#/moduleList"}
            ]
        },
        {
            displayName: "巡检管理", iconClass: "fa fa-stethoscope fa-lg",
            children: [
                {displayName: "新增任务", url: "#/taskAdd"},
                {displayName: "任务列表", url: "#/taskList"},
            ]
        },
        {
            displayName: "巡检报告", iconClass: "fa fa-tachometer fa-lg",
            children: [
                {displayName: "巡检报告", url: "#/reportSearch"},
                {displayName: "历史报告", url: "#/reportHistory"},
                // {displayName: "常用报表", url: "#/reportsList"},
            ]
        },
        // {
        //     displayName: "配置管理", iconClass: "fa fa-shield  fa-lg", url: "#/configList"
        // },
        {
            displayName: "系统管理", iconClass: "fa fa-cog fa-lg",
            children: [
                // {displayName: "全局设置", url: "#/sysSet"},
                // {displayName: "业务管理", url: "#/appList"},
                {displayName: "系统设置", url: "#/changeLogo"},
                {displayName: "自定义巡检项", url: "#/customItem"},
                // {displayName: "自定义配置项", url: "#/configList"},
                {displayName: "邮箱管理", url: "#/mailList"},
                {displayName: "操作日志", url: "#/logList"}
            ]
        }
    ];

    $scope.logo_img = site_url + "show_logo/";

    $scope.menuOption = {
        data: 'menuList',
        locationPlaceHolder: '#locationPlaceHolder',
        adaptBodyHeight: CWApp.HeaderHeight + CWApp.FooterHeight
    };

    sysService.update_url({
        app_path: app_path
    }, {}, function (res) {

    });
}]);