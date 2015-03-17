import json
from datetime import datetime, timedelta

from flask import Flask, request

from db import DataBase

DATE_FORMAT = '%Y-%m-%d'  # Format for parsing api date params
JSON_DATE_FORMAT = '%Y-%m-%dT00:00:00Z'  # Format for converting dates to JSON

app = Flask(__name__)
app.debug = True


# Map of metric_id's to friendly names
metric_id_to_name_map = {
    'unique_visitors': 'Unique Visitors',
    'page_views': 'Page Views',
    'visits': 'Visitors',
}


def ensure_data_for_missing_dates(data, start_date, end_date):
    """
    Checks the data for missing dates and fills gaps with zeros

    Params
    ------
    data: [[datetime.date, int], ...]
    start_date: datetime.date
    end_date: datetime.date

    Returns
    -------
    [int, ...]
    """
    raise NotImplementedError('TODO: ensure_data_for_missing_dates')


def transform_data_to_series(metric_id, data):
    """
    Prepares the metric and data to be sent as the API's response

    Params
    ------
    metric_id: string
        metric_id used to query the data
    data: [int, ...]

    Returns
    -------
    {
        'name': string  # Friendly metric name
        'total': int  # Sum of the data
        'data': [int, ...] # The data that was passed in

    }
    """
    raise NotImplementedError('TODO: transform_data_to_series')


def get_index(start_date, end_date):
    """
    Get the index for the requested range
    This is an array of dates from the start_date
    to the end_date inclusive

    This will be used as the x-axis labels for the chart

    Params
    ------
    start_date: datetime.date
    end_date: datetime.date

    Returns
    -------
    [datetime.date, ...]
    """
    raise NotImplementedError('TODO: get_index')


@app.route('/')
def root():
    """
    The root '/' route
    Serves the index.html file

    Static files are served automatically by flask
    """
    return app.send_static_file('index.html')


@app.route('/api')
def api():
    """
    Api endpoint at '/api'

    Fetches the data for the requested metrics and date range

    Query Params
    ------------
    start_date: string  # 'YYYY-mm-dd'
    end_date: string  #  'YYYY-mm-dd'
    metrics:  [metric_id, ...]
    """

    # We may want to do some sanity checking on the query params
    # What should be done in the event the params do not make sense?
    start_date = datetime.strptime(request.args.get('start_date'), DATE_FORMAT).date()
    end_date = datetime.strptime(request.args.get('end_date'), DATE_FORMAT).date()
    metrics = request.args.getlist('metrics')

    db = DataBase()

    response = {
        'index': get_index(start_date, end_date),
        'series': {}
    }

    for metric_id in metrics:
        data = db.get_data(metric_id, start_date, end_date)
        data = ensure_data_for_missing_dates(data, start_date, end_date)
        data = transform_data_to_series(metric_id, data)
        response['series'][metric_id] = data

    return json.dumps(response, indent=4)


# Start the api if calling directly
# $ python server.py
if __name__ == '__main__':
    app.run()
