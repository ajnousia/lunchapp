(function(){
  'use strict';

  angular
    .module('menugrid', ["ngMaterial"])
    .directive('menuGrid', ["$timeout", MenuGridDirective])
    .controller('MenuGridController', ["$http", "$timeout", MenuGridController]);

  function MenuGridDirective($timeout) {
    function link(scope, element, attrs, controller) {
      controller.restaurants = scope.date;
    }
    return {
      "restrict": 'E',
      "link": link,
      "templateUrl": './src/menugrid/view/menuGrid.html',
      "controller": MenuGridController,
      "scope": {
        "date": "="
      },
      "controllerAs": "mgctrl"
    }
  }

  function MenuGridController($http, $timeout) {
    var mgctrl = this;
    var gridTileContents = []
    var initialRowSpan = 10;
    mgctrl.gridRowHeight = 10; //px
    mgctrl.gridTiles = [];

    $http.get("./assets/menucard_dummy_data.json").success(function(data) {
    // $http.get('rest/query').success(function(data) {
      gridTileContents = reformatDummyData(data);
      gridTileContents.forEach(function(element, index) {
        var cardProperties = {};
        cardProperties["content"] = gridTileContents[index];
        cardProperties["rowspan"] = initialRowSpan;
        mgctrl.gridTiles.push(cardProperties);
      });
    });


    function reformatDummyData(data){
      for (var i = 0; i < data.menu.length; i++) {
        data.menu[i] = data.menu[i].split("\n");
      }
      var returnList = [];
      var numberOfRestaurants = mgctrl.restaurants;
      for (var i = 0; i < numberOfRestaurants; i++) {
        var randomShortValue = getRandomArbitrary(1, data.menu.length-1);
        returnList[i] = {};
        angular.copy(data, returnList[i]);
        returnList[i].menu = data.menu.slice(0, randomShortValue);
      }
      return returnList;
    }
  }



  function getRandomArbitrary(min, max) {
    return Math.random() * (max - min) + min;
  }


})();
