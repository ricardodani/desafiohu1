var myApp = angular.module("myApp", ["ngRoute", "ngResource", "myApp.services", 'mgcrea.ngStrap']);
var services = angular.module("myApp.services", ["ngResource"])
services
.factory('Places', function($resource) {
    return $resource('http://localhost:5000/places', {searchString: '@searchString'}, {
        query: { method: 'GET', isArray: true}
    });
})
.factory('Disp', function($resource) {
    return $resource('http://localhost:5000/disp', {
        placeId: '@placeId',
        placeType: '@placeType',
        enterDate: '@enterDate',
        exitDate: '@exitDate',
        undefinedDate: '@undefinedDate'
    }, {
        query: { method: 'GET', isArray: true}
    });
});

myApp.config(function($routeProvider) {
    $routeProvider
    .when('/', {
        templateUrl: 'pages/main.html',
        controller: 'mainController'
    })
})
.config(function($datepickerProvider) {
  angular.extend($datepickerProvider.defaults, {
    dateFormat: 'dd/MM/yyyy',
    startWeek: 1
  });
});

myApp.controller(
    'mainController',
    function ($scope, Places, Disp) {
        $scope.places = function() {
            searchString = $scope.searchString;
            if (searchString.length > 1) {
                $scope.places_results = Places.query({
                    searchString: searchString
                });
            } else {
                $scope.places_results = [];
            }
        };
        $scope.hotels = function() {
            $scope.disponibilities = Disp.query({
                placeId: $scope.placeId,
                placeType: $scope.placeType,
                enterDate: $scope.enterDate,
                exitDate: $scope.exitDate,
                undefinedDate: $scope.undefinedDate
            });
        };
        $scope.setPlaceValue = function(value) {
            $scope.searchString = value.name;
            $scope.placeId = value.id;
            $scope.placeType = value.type;
            $scope.places_results = [];
        };
    }
);
