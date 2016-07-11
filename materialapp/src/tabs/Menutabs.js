(function(){
  'use strict';

  angular
    .module('menutabs', ["ngMaterial"])
    .controller('MenuTabsController', [MenuTabsController]);

  function MenuTabsController() {
    var mtc = this;
    mtc.selectedIndex = 4 // function () {
    //   var date = new Date();
    //   if (date.getDay() == 0) {
    //     return 6;
    //   } else {
    //     return date.getDay()-1;
    //   }
    // }();

    console.log(mtc.selectedIndex);
  }

})();
