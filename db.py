from datetime import timedelta
from random import sample, randint


class DataBase(object):
    valid_metrics = {'unique_visitors', 'page_views', 'visits'}

    def get_data(self, metric_id, start_date, end_date):
        if metric_id not in self.valid_metrics:
            raise ValueError('Requested invalid column from database')

        delta_days = (end_date - start_date).days + 1
        dates = sample([
            (start_date + timedelta(day))
            for day in xrange(delta_days)
        ], randint(0, delta_days))

        return [[date, randint(0, 100)] for date in dates]
