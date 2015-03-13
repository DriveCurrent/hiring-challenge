from datetime import timedelta
from random import sample, randint


class DataBase(object):
    """
    Object emulating a database of metrics stored by dates_in_range

    Example
    -------
    >>> from datetime import date
    >>> db = DataBase()
    >>> db.get_data('unique_visitors', date(2015, 1, 1), date(2015, 1, 15))
    [[date(2015, 1, 1), 5], [date(2015, 1, 6), 5], [date(2015, 1, 9), 25]]

    >>> db.get_data('invalid', date(2015, 1, 1), date(2015, 1, 15))
    Exception: ValueError('Requested invalid column from database')
    """

    valid_metrics = {'unique_visitors', 'page_views', 'visits'}

    def get_data(self, metric_id, start_date, end_date):
        """
        Returns data for the requested metric between the start and end date

        Note: Data may not be available for all days

        Params
        ------
        metric_id: string
            one of the `valid_metrics`
        start_date: datetime.date
        end_date: datetime.date

        Returns
        -------
        [[datetime.date, int], ...]
        """

        if metric_id not in self.valid_metrics:
            raise ValueError('Requested invalid column from database')

        # Get the distance in days between start and end date
        delta_days = (end_date - start_date).days + 1

        # Generate a list of all the dates in between start and end
        dates_in_range = [
            (start_date + timedelta(day))
            for day in xrange(delta_days)
        ]
        # Make a list by choosing a random number of dates from the list
        # simulating that the database will not always have data
        # for certain dates
        dates_in_range = sample(dates_in_range, randint(0, delta_days))

        # Make rows of data for the dates were selected with the data being
        # a random integer between 0 and 100
        data = [[date, randint(0, 100)] for date in dates_in_range]

        return data
