var app = angular.module("myApp", ['myController', 'utilServices', 'myDirective', 'ui.bootstrap', 'ui.router', 'webApiService', 'cwLeftMenu', 'ngGrid']);
var controllers = angular.module("myController", []);
var directives = angular.module("myDirective", []);


app.config(["$stateProvider", "$urlRouterProvider", "$httpProvider", function ($stateProvider, $urlRouterProvider, $httpProvider) {
    $httpProvider.defaults.headers.post['X-CSRFToken'] = $("#csrf").val();
    $urlRouterProvider.otherwise("/home");//默认展示页面
    $stateProvider.state('home', {
        url: "/home",
        controller: "home",
        templateUrl: static_url + "client/views/home.html"
    })
        .state('taskList', {
            url: "/taskList",
            controller: "taskListCtrl",
            templateUrl: static_url + "client/views/taskManagement/taskList.html"
        })
        .state('taskAdd', {
            url: "/taskAdd",
            controller: "taskAddCtrl",
            templateUrl: static_url + "client/views/taskManagement/taskAdd.html"
        })
        .state('reportHistory', {
            url: "/reportHistory",
            controller: "reportHistory",
            templateUrl: static_url + "client/views/reportManagement/reportHistory.html"
        })
        .state('reportServer', {
            url: "/reportServer",
            controller: "reportServer",
            templateUrl: static_url + "client/views/reportManagement/reportServer.html"
        })
        .state('errorSummary', {
            url: "/errorSummary",
            controller: "errorSummary",
            templateUrl: static_url + "client/views/reportManagement/errorSummary.html"
        })
        .state('reportServerDetail', {
            url: "/reportServerDetail",
            controller: "reportServerDetail",
            templateUrl: static_url + "client/views/reportManagement/reportServerDetail.html"
        })
        .state('reportSearch', {
            url: "/reportSearch",
            controller: "reportServer",
            templateUrl: static_url + "client/views/reportManagement/reportServer.html"
        })

        .state('customItem', {
            url: "/customItem",
            controller: "customItemCtrl",
            templateUrl: static_url + "client/views/taskManagement/customItem.html"
        })
        .state('moduleAdd', {
            url: "/moduleAdd",
            controller: "moduleAddCtrl",
            templateUrl: static_url + "client/views/moduleManagement/moduleAdd.html"
        })
        .state('moduleList', {
            url: "/moduleList",
            controller: "moduleListCtrl",
            templateUrl: static_url + "client/views/moduleManagement/moduleList.html"
        })



        //系统管理
        .state('sysSet', {
            url: "/sysSet",
            controller: "sysSet",
            templateUrl: static_url + "client/views/sysManagement/sysSet.html"
        })
        // .state('test', {
        //     url: "/test",
        //     controller: "testCtrl",
        //     templateUrl: static_url + "client/views/test.html"
        // })
        // .state('configList', {
        //     url: "/configList",
        //     controller: "configList",
        //     templateUrl: static_url + "client/views/sysManagement/configList.html"
        // })
        .state('logList', {
            url: "/logList",
            controller: "logList",
            templateUrl: static_url + "client/views/sysManagement/logList.html"
        })
        .state('mailList', {
            url: "/mailList",
            controller: "mailList",
            templateUrl: static_url + "client/views/sysManagement/mailList.html"
        })
        .state('changeLogo', {
            url: "/changeLogo",
            controller: "changeLogoCtrl",
            templateUrl: static_url + "client/views/sysManagement/changeLogo.html"
        })
}]);


