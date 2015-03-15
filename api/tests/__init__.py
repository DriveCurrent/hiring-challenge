from datetime import date
from mock import patch, call
from unittest import TestCase

from db import DataBase


class APITestCase(TestCase):
    def setUp(self):
        self.delta_days = 2  # Distance between start and end date plus one
        self.valid_params = ('page_views', date(2015, 1, 1), date(2015, 1, 2),)

    def test_valid_metrics_list(self):
        valid_metrics = {'unique_visitors', 'page_views', 'visits'}
        self.assertEqual(DataBase.valid_metrics, valid_metrics)

    @patch('db.sample')
    @patch('db.randint')
    def test_returns_data_if_valid_metric(self, randint, sample):
        db = DataBase()
        self.mock_random_data = [1, 2]
        self.dates_in_range = [date(2015, 1, 1),  date(2015, 1, 2)]
        randint.side_effect = [self.delta_days] + self.mock_random_data
        expected_data = map(list, zip(self.dates_in_range, self.mock_random_data))
        sample.return_value = self.dates_in_range

        actual_data = db.get_data(*self.valid_params)

        randint.assert_has_calls([call(0, self.delta_days)] + [call(0, 100)] * 2)
        sample.assert_called_once_with(self.dates_in_range, 2)

        self.assertEqual(expected_data, actual_data)

    def test_will_raise_value_error_if_invalid_metric(self):
        (self.assertRaises(
            ValueError,
            DataBase().get_data,
            'invalid_metric', date(2015, 1, 1), date(2015, 1, 2)))
