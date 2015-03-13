(function() {
  'use strict';

  Chart.defaults.Line.datasetFill = false;

  var apiEndpoint = 'http://127.0.0.1:5000';

  function HiringChallengeController($http, $filter) {
    var colors = [
      '#f1595f',
      '#727272',
      '#79c36a',
    ];

    function dateToJson(date) {
      return date.toJSON().match(/\d{4}-\d{2}-\d{2}/)[0];
    }

    function jsonToDate(dateStr) {
      return $filter('date')(dateStr, 'd MMM', 'UTC');
    }

    function transformResponse(data) {
      var labels, datasets;

      labels = data.index.map(jsonToDate);

      datasets = Object.keys(data.series).map(function(key, i) {
        return {
          data: data.series[key].data,
          strokeColor: colors[i],
          pointColor: colors[i],
          pointHighlightStroke: colors[i],
          pointStrokeColor: '#fff',
          pointHighlightFill: '#fff',
        };
      });

      return {
        labels: labels,
        datasets: datasets
      };
    }

    this.updateData = function updateData() {
      var params = {
        start_date: dateToJson(this.start_date),
        end_date: dateToJson(this.end_date),
        metrics: 'visits'
      };

      $http
        .get(apiEndpoint, {params: params})
        .then((function(response) {
          this.chartData = transformResponse(response.data);
        }).bind(this));
    };

    // Fetch the initial data
    this.start_date = new Date('2015-01-01T00:00:00Z');
    this.end_date = new Date('2015-01-15T00:00:00Z');
    this.updateData();
  }

  HiringChallengeController.$inject = ['$http', '$filter'];

  angular
    .module('app', [])
    .directive('hiringChallenge', function() {
      return {
        bindToController: true,
        controller: HiringChallengeController,
        controllerAs: 'app',
        // scope: {}
      };
    })
    .directive('chart', function() {
      return {
        bindToController: true,
        // scope: {},
        link: function(scope, element) {
          // Get the context of the canvas element we want to select
          scope.$watch('app.chartData', function(data) {
            var context, chart;

            if (!data) return;

            context = element[0].getContext('2d'),
            chart = new Chart(context).Line(data);
          });
        }
      };
    });
}());
