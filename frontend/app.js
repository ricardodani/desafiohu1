var myApp = angular.module("myApp", ["ngRoute", "ngResource", "myApp.services", 'mgcrea.ngStrap']);
var services = angular.module("myApp.services", ["ngResource"])
services
.factory('Places', function($resource) {
    return $resource('http://localhost:5000/places', {searchString: '@searchString'}, {
        query: { method: 'GET', isArray: true}
    });
})
.factory('Hotel', function($resource) {
    return $resource('http://localhost:5000/hotel', {
        hotelId: '@hotelId',
        cityId: '@cityId',
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
});


myApp.controller(
    'mainController',
    function ($scope, Places, Hotel) {
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
            if ($scope.enterDate && $scope.exitDate) {
                $scope.hotel_results = Hotel.query({
                    enterDate: $scope.enterDate,
                    exitDate: $scope.exitDate,
                    undefinedDate: $scope.undefinedDate
                });
            }
        };
    }
);
