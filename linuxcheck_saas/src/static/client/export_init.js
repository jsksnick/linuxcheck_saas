var app = angular.module("exportApp", ['myController', 'utilServices', 'myDirective', 'ui.bootstrap', 'ui.router', 'webApiService','ngGrid']);
var controllers = angular.module("myController", []);
var directives = angular.module("myDirective", []);


app.config(["$stateProvider", "$urlRouterProvider", "$httpProvider", function ($stateProvider, $urlRouterProvider, $httpProvider) {
    $httpProvider.defaults.headers.post['X-CSRFToken'] = $("#csrf").val();
    // $urlRouterProvider.otherwise("/home");//默认展示页面
    // $stateProvider.state('reportServer', {
    //     url: "/reportServer",
    //     controller: "reportServer",
    //     templateUrl: static_url + "client/views/exportManagement/reportServer.html"
    // })
    // .state('reportServerDetail', {
    //     url: "/reportServerDetail",
    //     controller: "reportServerDetail",
    //     templateUrl: static_url + "client/views/exportManagement/reportServerDetail.html"
    // })
}]);


