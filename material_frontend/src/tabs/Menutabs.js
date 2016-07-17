(function(){
  'use strict';

  angular
    .module('menutabs', ["ngMaterial"])
    .controller('MenuTabsController', [MenuTabsController]);

  function MenuTabsController() {
    var mtc = this;
    mtc.selectedIndex = function () {
      var date = new Date();
      if (date.getDay() == 0) {
        return 6;
      } else {
        return date.getDay()-1;
      }
    }();
  }

})();
