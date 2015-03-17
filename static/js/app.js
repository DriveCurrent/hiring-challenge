(function() {
  'use strict';

  Chart.defaults.Line.datasetFill = false;

  function HiringChallengeController($http, $filter) {
    var colors = [
      '#f1595f',
      '#727272',
      '#79c36a',
    ];

    /**
     * Transforms a timestamp into a JSON formatted date string
     * @param  int date JS timestamp Ex: 1430438400
     * @return String EX: '2015-01-01T00:00:00Z'
     */
    function dateToJson(date) {
      return date.toJSON().match(/\d{4}-\d{2}-\d{2}/)[0];
    }

    /**
     * Transforms a JSON formatted date string
     * into a human readable string
     *
     * @param  String  datestr Ex: '2015-01-01T00:00:00Z'
     * @return String EX: '1 Jan'
     */
    function jsonToDateStr(dateStr) {
      return $filter('date')(dateStr, 'd MMM', 'UTC');
    }

    /**
     * Helper function to process data from the api
     * and transform it into a format that ChartJS can work with
     *
     * @param  data API response
     *   {
     *     index: [timestamp, ...],
     *     series: {
     *       metric_id: {
     *         data: [int, ...]
     *       }
     *     },
     *   }
     * @return ChartJS config object
     */
    function transformResponse(data) {
      var labels, datasets;

      labels = data.index.map(jsonToDateStr);

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

    /**
     * Gets data from the api and publish it to this.chartData
     *
     * Request should be made to '/api' and include
     * start_date, end_date, and metrics query parameters
     */
    this.updateData = (function updateData() {
      throw Error('TODO: updateData - Not Implemented.');
    });

    // Default Values
    this.start_date = new Date('2015-01-01T00:00:00Z');
    this.end_date = new Date('2015-01-15T00:00:00Z');
    this.metrics = {
      unique_visitors: 'unique_visitors',
      page_views: 'page_views',
      visits: 'visits',
    };

    // Fetch the initial data
    throw Error('TODO: Fetch inital data');
  }

  HiringChallengeController.$inject = ['$filter'];

  angular
    .module('app', [])
    .directive('hiringChallenge', function() {
      return {
        bindToController: true,
        controller: HiringChallengeController,
        controllerAs: 'app',
      };
    })
    .directive('chart', function() {
      return {
        bindToController: true,
        scope: {
          chart: '='
        },
        link: function(scope, element) {
          // Get the context of the canvas element we want to select
          scope.$watch('chart', function(data) {
            var context, chart;

            if (!data || !data.datasets.length) return;

            context = element[0].getContext('2d');
            chart = new Chart(context).Line(data);
          });
        }
      };
    });
}());
