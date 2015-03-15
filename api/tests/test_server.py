import json
from unittest import TestCase

import server


class APITestCase(TestCase):
    def build_endpoint(self, start_date, end_date, metrics):
        metrics = '&metrics='.join(metrics)

        url = '/?start_date={}&end_date={}&metrics={}'.format(
            start_date, end_date, metrics)

        print url

        return url

    def setUp(self):
        server.app.config['TESTING'] = True
        self.app = server.app.test_client()

        self.valid_metrics = ['visits', 'unique_visitors', 'page_views']
        self.response = self.app.get(
            self.build_endpoint(
                start_date='2015-01-01',
                end_date='2015-01-02',
                metrics=self.valid_metrics
            )
        )
        self.response_data = json.loads(self.response.data)

    def test_status_returns_200(self):
        """
        Simple check to make sure the api returns without failing
        """
        self.assertEqual(self.response.status_code, 200)

    def test_index_should_contain_all_dates_in_range(self):
        expected_index = ['2015-01-01T00:00:00Z', '2015-01-02T00:00:00Z']
        self.assertEqual(self.response_data['index'], expected_index)

    def test_series_should_contain_an_entry_for_each_metric(self):
        self.assertItemsEqual(self.response_data['series'].keys(), self.valid_metrics)
