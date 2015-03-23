(function() {
    'use strict';

    Chart.defaults.Line.datasetFill = false;

    function HiringChallengeController($http, $filter, $resource) {

        // Created in order to avoid scoping issues with REST functions
        var _this = this;

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
                    label: key,
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

        // Default Values
        this.start_date = new Date('2015-01-01T00:00:00Z');
        this.end_date = new Date('2015-01-15T00:00:00Z');
        this.metrics = {
            unique_visitors: "unique_visitors",
            page_views: "page_views",
            visits: "visits",
        };

        // Pulls data from API with defaults
        this.dataGet = $resource('/api?start_date=:start_date&end_date=:end_date', {
            start_date: dateToJson(_this.start_date),
            end_date: dateToJson(_this.end_date),
            metrics: [
                _this.metrics.unique_visitors,
                _this.metrics.page_views,
                _this.metrics.visits
            ]

        });

        // _this.tempData = [];

        _this.tempData = {};

        _this.updateMetrics = function updateMetrics(metric) {
            var chart = window.chart;

            for (var key in chart.datasets) {
              if (chart.datasets[key].label === metric[0]) {
                _this.tempData[key] = _.clone(chart.datasets[key]);
                delete chart.datasets[key];
                console.log(_this.tempData);
              } else {
                chart.datasets.push(_.clone(_this.tempData[key]));
                delete _this.tempData[key];
              }
              
            }

            // Remove falsy values from chart data array to keep chart alive
            chart.datasets = _.compact(chart.datasets);

        };


        // Generate the initial dataset
        this.dataSet = this.dataGet.get({},
            function(successResponse) {

                var data = transformResponse(successResponse);

                // Build initial chart
                _this.chartData = {
                    labels: data.labels,
                    datasets: data.datasets
                };

            },
            function(errorResponse) {
                console.log(errorResponse);
            }
        );

        this.updateData = (function updateData() {

            function checkMetrics(metrics) {
                var used_metrics = [];
                for (var key in _this.metrics) {
                    if (_this.metrics[key] !== false) {
                        used_metrics.push(_this.metrics[key]);
                    }
                }
                return used_metrics;
            }

            // Update data on web page
            _this.dataGet.get({
                    start_date: dateToJson(_this.start_date),
                    end_date: dateToJson(_this.end_date),
                    metrics: checkMetrics(_this.metrics)
                },
                function(successResponse) {
                    var data = transformResponse(successResponse);
                    _this.chartData = {
                        labels: data.labels,
                        datasets: data.datasets
                    };
                    // Refresh graph data
                    window.chart.destroy();
                },
                function(failureResponse) {
                    console.log(failureResponse);
                });
        });

    }

    HiringChallengeController.$inject = ['$http', '$filter', '$resource'];

    angular
        .module('app', ['ngResource'])
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

                        for (var key in data.datasets) {
                          if (data.datasets[key].visible === false) {
                            data.datasets.pop(key);
                          }
                        }

                        context = element[0].getContext('2d');
                        chart = new Chart(context).Line(data);
                        window.chart = chart;

                    });
                }
            };
        });
}());