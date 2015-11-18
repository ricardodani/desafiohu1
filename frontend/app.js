var myApp = angular.module("myApp", ["ngRoute", "ngResource", "myApp.services"]);
var services = angular.module("myApp.services", ["ngResource"])
services
.factory('Places', function($resource) {
    return $resource('http://localhost:5000/api/v1/places', {searchString: '@searchString'}, {
        query: { method: 'GET', isArray: true}
    });
})
.factory('Hotel', function($resource) {
    return $resource('http://localhost:5000/api/v1/hotel', {cityId: '@cityId', 
                                                            enterDate: '@enterDate',
                                                            exitDate: '@exitDate'}, {
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
        $scope.placesSearch = function() {
            if ($scope.searchString > 1) {
                $scope.place_suggestions = Places.query({ searchString: $scope.searchString });
            }
        };
        $scope.hotelSearch = function() {
            if ($scope.enterDate && $scope.exitDate) {
                $scope.hotel_results = Hotel.query({
                    cityId: $scope.cityId,
                    enterDate: $scope.enterDate,
                    exitDate: $scope.exitDate
                });
            }
        };
    }
);
