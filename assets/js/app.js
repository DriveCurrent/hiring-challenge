(function() {

  Chart.defaults.Line.datasetFill = false;

  var apiEndpoint = 'http://127.0.0.1:5000';

  function HiringChallengeController($http) {
    var colors = [
      '#727272',
      '#f1595f',
      '#79c36a',
    ];

    function transformResponse(response) {
      data = {
        labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July'],
        datasets: [
          {
            pointStrokeColor: '#fff',
            pointHighlightFill: '#fff',
            data: [65, 59, 80, 81, 56, 55, 40]
          },
          {
            pointStrokeColor: '#fff',
            pointHighlightFill: '#fff',
            data: [28, 48, 40, 19, 86, 27, 90]
          }
        ],
      };

      data.datasets.forEach(function(dataset, i) {
        dataset.strokeColor = colors[i];
        dataset.pointColor = colors[i];
        dataset.pointHighlightStroke = colors[i];
      });

      return data;
    }

    this.updateData = function updateData() {
      var params = {};
      this.chartData = transformResponse();
      // $http
      //   .get(apiEndpoint, params)
      //   .then(function(data) {
      //     debugger;
      //     this.chartData = transformResponse(data);
      //   });
    };

    // Fetch the initial data
    this.updateData();
  }

  HiringChallengeController.$inject = ['$http'];

  angular
    .module('app', [])
    .directive('hiringChallenge', function() {
      return {
        bindToController: true,
        controller: HiringChallengeController,
        controllerAs: 'app',
        scope: {},
        link: function(scope, element) {
          // Get the context of the canvas element we want to select
          scope.$watch('app.chartData', function(data) {
            var
              context = element.find('canvas')[0].getContext('2d'),
              chart = new Chart(context).Line(data);
          });
        }
      };
    });
}());
