var myApp = angular.module('myApp', [],function($interpolateProvider) {
    $interpolateProvider.startSymbol('[{');
    $interpolateProvider.endSymbol('}]');
});


myApp.controller("featureController", function ($scope, $http) {
    $scope.clients = ["Client-A","Client-B","Client-C","Client-D"];
    $scope.selectedClient = $scope.clients[0];
    $scope.maxPriority = 10;
    $scope.products = ["Policies","Billing","Claims","Reports"];
    $scope.features = [];

    $scope.selectedFeature = {
        "title" : "",
        "description" :'',
        "client" :$scope.clients[0],
        "client_priority":1,
        "target_date":"",
        "product_area":$scope.products[0]
    };

    $scope.get_features = function(){
        $http.get("/api/feature/")
             .then(function(response){
                 console.log(response);
                 $scope.features = response.data;
             });
    };
    $scope.get_features();

    $scope.submitFeature = function () {
        console.log($scope.selectedFeature);
        $http({
            method  : 'POST',
            url     : '/api/feature/',
            data    : $.param($scope.selectedFeature),
            headers : { 'Content-Type': 'application/x-www-form-urlencoded' }
        }).success(function(data) {
            console.log("successfully added");
            new Noty({text: 'successfully added',
                type:"success",
                timeout:3000
            }).show();
            $scope.get_features();
            $('#modalFeatureForm').modal('toggle');
        }).error(function (err) {
            console.log("error due to : ",err);
            new Noty({text: 'Error due to '+JSON.stringify(err),
                type:"error",
                timeout:60000
            }).show();
        });
    };



});

myApp.filter('range', function(){
    return function(n) {
      var res = [];
      for (var i = 1; i <= n; i++) {
        res.push(i);
      }
      return res;
    };
  });
myApp.config(['$httpProvider', function($httpProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
}]);


$(document).ready(function(){
    $('#traget_date').datepicker({
        format: 'yyyy-mm-dd'
    });
});
