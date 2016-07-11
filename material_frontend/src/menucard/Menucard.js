(function() {
  'use strict';

  angular
        .module('menucard' , ["ngMaterial"])
        .directive('menuCard', ["$timeout", MenuCardDirective]);

  function MenuCardDirective($timeout) {
    function link(scope, element){
      $timeout(function() {
        var height = element[0].offsetHeight;
        var rowSpan = Math.ceil(height/scope.rowHeight);
        scope.gridTiles[scope.index]["rowspan"] = rowSpan;
      });
    }
    return {
      "restrict": 'E',
      "link": link,
      "scope": {
        'gridTiles': '=data',
        "index": "=",
        "rowHeight": "=rowheight"
      },
      "templateUrl": "./src/menucard/view/menuCard.html"
    };
  }

})();
