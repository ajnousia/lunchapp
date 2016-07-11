(function(){
  'use strict';

  angular
    .module('menubar', ["ngMaterial"])
    .directive('menuBar', MenuBarDirective)
    .controller('MenuBarController', MenuBarController);


  function MenuBarController() {

  }

  function MenuBarDirective(){
    return {
      "restrict": 'E',
      "templateUrl": './src/menubar/view/menuBar.html',
      "controller": MenuBarController,
      "controllerAs": "mbctrl"
    }
  }

})();
